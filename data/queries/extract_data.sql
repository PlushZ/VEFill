-- Extract DMS scores and related features
SELECT
    g.id AS gene_id,
    m.id AS mutation_id,
    m.position,
    m.wt_residue,
    m.variant_residue,
    m.eve_score,
    m.eve_class_75_set,
    sm.blosum62,
    sm.grantham,
    sm.pam70,
    sm.rao,
    sm.risler,
    sm.str,
    sm.benner22,
    sm.benner6,
    sm.benner74,
    sm.blastp,
    sm.blosum45,
    sm.blosum50,
    sm.blosum80,
    sm.blosum90,
    sm.dayhoff,
    sm.feng,
    sm.genetic,
    sm.gonnet1992,
    sm.johnson,
    sm.jones,
    sm.levin,
    sm.mclachlan,
    sm.mdm78,
    sm.pam250,
    sm.pam30,
    dms.score AS dms_score,
    g.assay_type,
    dr.synonymous_from_method AS wt_score,
    dr.nonsense_from_method AS non_score,
    m.edit_distance,
    m.alphamissense_pathogenicity,
    m.alphafold_conf_type,
    mt.type AS mutation_type,
    aa_wt.chemical AS wt_chemical,
    aa_variant.chemical AS variant_chemical,
    aa_wt.charge AS wt_charge,
    aa_variant.charge AS variant_charge,
    aa_wt.hydrophobic AS wt_hydrophobic,
    aa_variant.hydrophobic AS variant_hydrophobic,
    aa_wt.stabilizing_interaction AS wt_stabilizing_interaction,
    aa_variant.stabilizing_interaction AS variant_stabilizing_interaction,
    aa_wt.volume AS wt_volume,
    aa_variant.volume AS variant_volume,
    aa_wt.h_bond_donor AS wt_h_bond_donor,
    aa_variant.h_bond_donor AS variant_h_bond_donor,
    aa_wt.h_bond_acceptor AS wt_h_bond_acceptor,
    aa_variant.h_bond_acceptor AS variant_h_bond_acceptor,
    aa_wt.solvent_accessible AS wt_solvent_accessible,
    aa_variant.solvent_accessible AS variant_solvent_accessible,
    aa_wt.redox_reactivity AS wt_redox_reactivity,
    aa_variant.redox_reactivity AS variant_redox_reactivity,
    aa_wt.amphipathic AS wt_amphipathic,
    aa_variant.amphipathic AS variant_amphipathic,
    aa_wt.polar AS wt_polar,
    aa_variant.polar AS variant_polar,
    aa_wt.molecular_weight_da AS wt_molecular_weight_da,
    aa_variant.molecular_weight_da AS variant_molecular_weight_da,
    aa_wt.pka25_co2h AS wt_pka25_co2h,
    aa_variant.pka25_co2h AS variant_pka25_co2h,
    aa_wt.pka25_nh2 AS wt_pka25_nh2,
    aa_variant.pka25_nh2 AS variant_pka25_nh2,
    aa_wt.isoelectric_point_pl AS wt_isoelectric_point_pl,
    aa_variant.isoelectric_point_pl AS variant_isoelectric_point_pl,
    aa_wt.hydropathy_index AS wt_hydropathy_index,
    aa_variant.hydropathy_index AS variant_hydropathy_index,
    e1.embedding AS embedding_wt,
    e2.embedding AS embedding_variant,
    e3.embedding AS embedding_difference
FROM
    mutation m
JOIN
    substitution_matrix sm
    ON sm.amino_acid_x = m.wt_residue AND sm.amino_acid_y = m.variant_residue
JOIN
    dms
    ON dms.mutation_id = m.id
JOIN
    gene_urn g
    ON m.gene_urn_id = g.id
JOIN
    assay a
    ON g.assay_type = a.id
JOIN 
    dms_range dr 
    ON g.id = dr.gene_urn_id
JOIN
    mutation_type mt
    ON m.mutation_type_id = mt.id
LEFT JOIN
    amino_acid_property aa_wt
    ON aa_wt.one_letter_code = m.wt_residue
LEFT JOIN
    amino_acid_property aa_variant
    ON aa_variant.one_letter_code = m.variant_residue
LEFT JOIN
    esm1v_embeddings e1
    ON e1.mutation_id = m.id AND e1.embedding_type = 'WT'
LEFT JOIN
    esm1v_embeddings e2
    ON e2.mutation_id = m.id AND e2.embedding_type = 'Variant'
LEFT JOIN
    esm1v_embeddings e3
    ON e3.mutation_id = m.id AND e3.embedding_type = 'Difference'
WHERE
    dms.score IS NOT NULL
    AND m.eve_score != 'NaN'
    AND dr.synonymous_from_method IS NOT NULL
    AND dr.nonsense_from_method IS NOT NULL
    AND g.id IN (552, 555, 559, 585, 587, 592, 595, 596, 597, 598, 600, 601, 602, 606, 611, 613, 623, 632, 634, 635,
        637, 638, 643, 658, 659, 660, 665, 667, 668, 672, 674, 675, 676, 680, 681, 682, 683, 684, 685, 687, 
        697, 698, 699, 700, 703, 707, 716, 717, 718, 720, 737, 740, 744, 750, 766, 770, 771, 779, 781, 782, 
        783, 785, 788, 789, 790, 794, 795, 797, 805, 807, 809, 818, 819, 823, 825, 827, 832, 841, 844, 847, 
        853, 855, 863, 864, 869, 872, 875, 876, 877, 878, 881, 884, 887, 888, 891, 900, 904, 909, 911, 913, 
        914, 915, 916, 917, 918, 919, 922, 924, 925, 926, 927, 928, 930, 931, 932, 936, 937, 938, 939, 943, 
        945, 948, 951, 963, 965, 968, 972, 976, 978, 988, 990, 994, 995, 1002, 1004, 1005, 1019, 1035, 1045, 1046);
        -- non-domainome gene_ids: (7, 10, 100, 109, 126, 197, 215, 505)
