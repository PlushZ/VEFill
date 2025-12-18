from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    ForeignKey,
    String,
    Boolean,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


# ---------------------------------------------------------------------
# Core reference tables
# ---------------------------------------------------------------------

class Assay(Base):
    __tablename__ = "assay"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Text, nullable=False)

    gene_urns = relationship("GeneURN", back_populates="assay")


class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True, autoincrement=True)
    species_name = Column(Text, nullable=False, unique=True)

    mutations = relationship("Mutation", back_populates="species")


class MutationType(Base):
    __tablename__ = "mutation_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False, unique=True)

    mutations = relationship("Mutation", back_populates="mutation_type")


# ---------------------------------------------------------------------
# Gene / mutation hierarchy
# ---------------------------------------------------------------------

class GeneURN(Base):
    __tablename__ = "gene_urn"

    id = Column(Integer, primary_key=True, autoincrement=True)
    urn_mavedb = Column(Text, unique=True)
    gene_name = Column(Text)
    target_seq = Column(Text)
    target_aa_seq = Column(Text)
    uniprot_id = Column(Text, nullable=True)
    ensembl_id = Column(Text, nullable=True)
    uniprot_target_seq_offset = Column(Integer, nullable=True)

    assay_type = Column(Integer, ForeignKey("assay.id"), nullable=True)

    assay = relationship("Assay", back_populates="gene_urns")
    mutations = relationship("Mutation", back_populates="gene_urn")
    dms_range = relationship("DmsRange", back_populates="gene_urn", uselist=False)


class Mutation(Base):
    __tablename__ = "mutation"

    id = Column(Integer, primary_key=True, autoincrement=True)

    gene_urn_id = Column(Integer, ForeignKey("gene_urn.id"))
    species_id = Column(Integer, ForeignKey("species.id"))
    mutation_type_id = Column(Integer, ForeignKey("mutation_type.id"))

    position = Column(Integer)
    wt_residue = Column(Text)
    variant_residue = Column(Text)
    edit_distance = Column(Integer)

    eve_score = Column(Float, nullable=True)
    eve_class_75_set = Column(Text, nullable=True)
    clinvar_label = Column(Text, nullable=True)
    alphamissense_pathogenicity = Column(Float, nullable=True)
    alphamissense_class = Column(Text, nullable=True)
    alphafold_conf_type = Column(Text, nullable=True)

    gene_urn = relationship("GeneURN", back_populates="mutations")
    species = relationship("Species", back_populates="mutations")
    mutation_type = relationship("MutationType", back_populates="mutations")

    esm1v_embeddings = relationship(
        "ESM1vEmbedding", back_populates="mutation", cascade="all, delete-orphan"
    )
    dms_entries = relationship("DMS", back_populates="mutation")
    msa = relationship("MSA", back_populates="mutation", uselist=False)


# ---------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------

class ESM1vEmbedding(Base):
    __tablename__ = "esm1v_embeddings"

    __table_args__ = (
        UniqueConstraint("mutation_id", "embedding_type", name="unique_mutation_type"),
        CheckConstraint(
            "embedding_type IN ('WT', 'Variant', 'Difference')",
            name="esm1v_embeddings_embedding_type_check",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    mutation_id = Column(Integer, ForeignKey("mutation.id"), nullable=False)
    embedding_type = Column(Text, nullable=False)
    embedding = Column(JSONB, nullable=False)

    mutation = relationship("Mutation", back_populates="esm1v_embeddings")


# ---------------------------------------------------------------------
# DMS
# ---------------------------------------------------------------------

class DmsRange(Base):
    __tablename__ = "dms_range"

    __table_args__ = (
        UniqueConstraint("gene_urn_id", name="dms_range_gene_urn_id_unique"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    gene_urn_id = Column(Integer, ForeignKey("gene_urn.id"))

    nonsense_from_data = Column(Float)
    max_hyperactivity = Column(Float)
    synonymous_from_data = Column(Float)
    calc_method = Column(String(255))
    nonsense_from_method = Column(Float)
    synonymous_from_method = Column(Float)
    min_from_data = Column(Float)
    max_from_data = Column(Float)

    gene_urn = relationship("GeneURN", back_populates="dms_range")
    dms_entries = relationship("DMS", back_populates="dms_range")


class DMS(Base):
    __tablename__ = "dms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mutation_id = Column(Integer, ForeignKey("mutation.id"))
    dms_range_id = Column(Integer, ForeignKey("dms_range.id"))
    score = Column(Float)

    mutation = relationship("Mutation", back_populates="dms_entries")
    dms_range = relationship("DmsRange", back_populates="dms_entries")


# ---------------------------------------------------------------------
# MSA
# ---------------------------------------------------------------------

class MSA(Base):
    __tablename__ = "msa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mutation_id = Column(Integer, ForeignKey("mutation.id"))

    shannon_entropy = Column(Float)
    jsd = Column(Float)
    phylop = Column(Float)
    phastcons = Column(Float)
    gerp = Column(Float)
    percentage_identity = Column(Float)
    ci = Column(Float)
    variant_percentage_residue = Column(Float)

    mutation = relationship("Mutation", back_populates="msa")


# ---------------------------------------------------------------------
# Substitution matrices
# ---------------------------------------------------------------------

class SubstitutionMatrix(Base):
    __tablename__ = "substitution_matrix"

    amino_acid_x = Column(Text, primary_key=True)
    amino_acid_y = Column(Text, primary_key=True)

    benner22 = Column(Float)
    benner6 = Column(Float)
    benner74 = Column(Float)
    blastn = Column(Float)
    blastp = Column(Float)
    blosum45 = Column(Float)
    blosum50 = Column(Float)
    blosum62 = Column(Float)
    blosum80 = Column(Float)
    blosum90 = Column(Float)
    blosum100 = Column(Float)
    dayhoff = Column(Float)
    feng = Column(Float)
    genetic = Column(Float)
    gonnet1992 = Column(Float)
    johnson = Column(Float)
    jones = Column(Float)
    levin = Column(Float)
    mclachlan = Column(Float)
    mdm78 = Column(Float)
    megablast = Column(Float)
    nuc_4_4 = Column(Float)
    pam250 = Column(Float)
    pam30 = Column(Float)
    pam70 = Column(Float)
    rao = Column(Float)
    risler = Column(Float)
    str = Column(Float)
    grantham = Column(Float)

    blosum62_minmax_scaled = Column(Text)
    pam250_minmax_scaled = Column(Text)


# ---------------------------------------------------------------------
# Amino acid properties
# ---------------------------------------------------------------------

class AminoAcidProperty(Base):
    __tablename__ = "amino_acid_property"

    id = Column(Integer, primary_key=True, autoincrement=True)

    one_letter_code = Column(String(1), nullable=False, unique=True)
    three_letter_code = Column(String(3), nullable=False, unique=True)
    full_name = Column(String(50), nullable=False)

    chemical = Column(Text, nullable=False)
    charge = Column(Text)
    hydrophobic = Column(Boolean, nullable=False)
    molecular_weight_da = Column(Float)
    isoelectric_point_pl = Column(Float)
    polar = Column(Boolean, nullable=False)
    volume = Column(Text, nullable=False)
    hydropathy_index = Column(Float)
    h_bond_donor = Column(Boolean, nullable=False)
    h_bond_acceptor = Column(Boolean, nullable=False)
    secondary_structure_preference = Column(Text)
    solvent_accessible = Column(Boolean, nullable=False)
    pka25_sidechain = Column(Float)
    redox_reactivity = Column(Boolean, nullable=False)
    amphipathic = Column(Boolean, nullable=False)
    stabilizing_interaction = Column(Text)
    pka25_co2h = Column(Float)
    pka25_nh2 = Column(Float)
