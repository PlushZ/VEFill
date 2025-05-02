import torch
import esm
import numpy as np
from db.orm.models import GeneURN, Mutation, ESM1vEmbedding
from db.orm.session import get_session
import db.config as config

# Database setup
session = get_session()

# Load pretrained ESM-1v model and alphabet
model, alphabet = esm.pretrained.load_model_and_alphabet_local(config.ESM_MODEL_PATH)
batch_converter = alphabet.get_batch_converter()
model.eval()

for gene_id in config.GENE_IDS:
    gene = session.query(GeneURN).filter(GeneURN.id == gene_id).first()
    if not gene or not gene.target_aa_seq:
        continue

    sequence_label = gene.gene_name or f"gene_{gene.id}"
    sequence = gene.target_aa_seq[: config.MAX_SEQ_LENGTH]
    seq_len = len(sequence)

    if seq_len < 1:
        continue

    # Convert full sequence to tokens for ESM embedding
    batch_labels, batch_strs, batch_tokens = batch_converter(
        [(sequence_label, sequence)]
    )

    with torch.no_grad():
        token_representations = model(
            batch_tokens, repr_layers=[33], return_contacts=False
        )
        residue_embeddings = token_representations["representations"][33][
            0, 1 : seq_len + 1
        ]

    # Pre-cache WT embeddings for difference calculation
    wt_embeddings = {}

    mutations = (
        session.query(Mutation).filter(Mutation.gene_urn_id == gene.id).distinct().all()
    )
    for mutation in mutations:
        pos = mutation.position
        if not (1 <= pos <= seq_len):
            continue

        wt_embed = residue_embeddings[pos - 1].tolist()
        wt_embeddings[mutation.id] = wt_embed

        session.add(
            ESM1vEmbedding(
                mutation_id=mutation.id,
                embedding_type="WT",
                embedding=wt_embed,
            )
        )

    session.commit()

    # Compute and store Variant and Difference embeddings
    for mutation in mutations:
        pos = mutation.position
        aa = mutation.variant_residue

        if not (1 <= pos <= seq_len) or not aa or len(aa) != 1:
            continue

        mutated_seq = sequence[: pos - 1] + aa + sequence[pos:]

        if "*" in mutated_seq:
            continue

        batch_labels, batch_strs, batch_tokens = batch_converter(
            [(sequence_label, mutated_seq)]
        )
        with torch.no_grad():
            token_representations = model(
                batch_tokens, repr_layers=[33], return_contacts=False
            )
            variant_embedding = token_representations["representations"][33][
                0, pos
            ].tolist()

        session.add(
            ESM1vEmbedding(
                mutation_id=mutation.id,
                embedding_type="Variant",
                embedding=variant_embedding,
            )
        )

        if mutation.id in wt_embeddings:
            diff_embedding = (
                np.array(variant_embedding) - np.array(wt_embeddings[mutation.id])
            ).tolist()
            session.add(
                ESM1vEmbedding(
                    mutation_id=mutation.id,
                    embedding_type="Difference",
                    embedding=diff_embedding,
                )
            )

    session.commit()

session.close()
