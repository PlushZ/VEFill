--
-- PostgreSQL database dump
--

-- Dumped from database version 14.19 (Ubuntu 14.19-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.19 (Ubuntu 14.19-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: amino_acid_property; Type: TABLE; Schema: public; Owner: polina_py
--

CREATE TABLE public.amino_acid_property (
    id integer NOT NULL,
    one_letter_code character varying(1) NOT NULL,
    three_letter_code character varying(3) NOT NULL,
    full_name character varying(50) NOT NULL,
    chemical text NOT NULL,
    charge text,
    hydrophobic boolean NOT NULL,
    molecular_weight_da double precision,
    isoelectric_point_pl double precision,
    polar boolean NOT NULL,
    volume text NOT NULL,
    hydropathy_index double precision,
    h_bond_donor boolean NOT NULL,
    h_bond_acceptor boolean NOT NULL,
    secondary_structure_preference text,
    solvent_accessible boolean NOT NULL,
    pka25_sidechain double precision,
    redox_reactivity boolean NOT NULL,
    amphipathic boolean NOT NULL,
    stabilizing_interaction text,
    pka25_co2h double precision,
    pka25_nh2 double precision
);


ALTER TABLE public.amino_acid_property OWNER TO polina_py;

--
-- Name: amino_acid_property_id_seq; Type: SEQUENCE; Schema: public; Owner: polina_py
--

CREATE SEQUENCE public.amino_acid_property_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.amino_acid_property_id_seq OWNER TO polina_py;

--
-- Name: amino_acid_property_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: polina_py
--

ALTER SEQUENCE public.amino_acid_property_id_seq OWNED BY public.amino_acid_property.id;


--
-- Name: assay; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assay (
    id integer NOT NULL,
    type text NOT NULL
);


ALTER TABLE public.assay OWNER TO postgres;

--
-- Name: assay_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.assay_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assay_id_seq OWNER TO postgres;

--
-- Name: assay_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.assay_id_seq OWNED BY public.assay.id;


--
-- Name: dms; Type: TABLE; Schema: public; Owner: polina
--

CREATE TABLE public.dms (
    id integer NOT NULL,
    mutation_id integer,
    score double precision,
    dms_range_id integer
);


ALTER TABLE public.dms OWNER TO polina;

--
-- Name: dms_dms_id_seq; Type: SEQUENCE; Schema: public; Owner: polina
--

CREATE SEQUENCE public.dms_dms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dms_dms_id_seq OWNER TO polina;

--
-- Name: dms_dms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: polina
--

ALTER SEQUENCE public.dms_dms_id_seq OWNED BY public.dms.id;


--
-- Name: dms_range; Type: TABLE; Schema: public; Owner: polina
--

CREATE TABLE public.dms_range (
    id integer NOT NULL,
    gene_urn_id integer,
    nonsense_from_data numeric,
    max_hyperactivity numeric,
    synonymous_from_data numeric,
    calc_method character varying(255),
    nonsense_from_method double precision,
    synonymous_from_method double precision,
    min_from_data double precision,
    max_from_data double precision
);


ALTER TABLE public.dms_range OWNER TO polina;

--
-- Name: dms_range_dms_range_id_seq; Type: SEQUENCE; Schema: public; Owner: polina
--

CREATE SEQUENCE public.dms_range_dms_range_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dms_range_dms_range_id_seq OWNER TO polina;

--
-- Name: dms_range_dms_range_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: polina
--

ALTER SEQUENCE public.dms_range_dms_range_id_seq OWNED BY public.dms_range.id;


--
-- Name: esm1v_embeddings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.esm1v_embeddings (
    id integer NOT NULL,
    mutation_id integer,
    embedding_type text,
    embedding jsonb NOT NULL,
    CONSTRAINT esm1v_embeddings_embedding_type_check CHECK ((embedding_type = ANY (ARRAY['WT'::text, 'Variant'::text, 'Difference'::text])))
);


ALTER TABLE public.esm1v_embeddings OWNER TO postgres;

--
-- Name: esm1v_embeddings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.esm1v_embeddings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.esm1v_embeddings_id_seq OWNER TO postgres;

--
-- Name: esm1v_embeddings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.esm1v_embeddings_id_seq OWNED BY public.esm1v_embeddings.id;


--
-- Name: gene_urn; Type: TABLE; Schema: public; Owner: polina
--

CREATE TABLE public.gene_urn (
    id integer NOT NULL,
    urn_mavedb text,
    gene_name text,
    target_seq text,
    uniprot_id text,
    ensembl_id text,
    uniprot_target_seq_offset integer,
    assay_type integer,
    target_aa_seq text
);


ALTER TABLE public.gene_urn OWNER TO polina;

--
-- Name: gene_urn_gene_urn_id_seq; Type: SEQUENCE; Schema: public; Owner: polina
--

CREATE SEQUENCE public.gene_urn_gene_urn_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gene_urn_gene_urn_id_seq OWNER TO polina;

--
-- Name: gene_urn_gene_urn_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: polina
--

ALTER SEQUENCE public.gene_urn_gene_urn_id_seq OWNED BY public.gene_urn.id;


--
-- Name: msa; Type: TABLE; Schema: public; Owner: polina
--

CREATE TABLE public.msa (
    id integer NOT NULL,
    mutation_id integer,
    shannon_entropy double precision,
    jsd double precision,
    phylop double precision,
    phastcons double precision,
    gerp double precision,
    percentage_identity double precision,
    ci double precision,
    variant_percentage_residue double precision
);


ALTER TABLE public.msa OWNER TO polina;

--
-- Name: msa_msa_id_seq; Type: SEQUENCE; Schema: public; Owner: polina
--

CREATE SEQUENCE public.msa_msa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.msa_msa_id_seq OWNER TO polina;

--
-- Name: msa_msa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: polina
--

ALTER SEQUENCE public.msa_msa_id_seq OWNED BY public.msa.id;


--
-- Name: mutation; Type: TABLE; Schema: public; Owner: polina
--

CREATE TABLE public.mutation (
    id integer NOT NULL,
    gene_urn_id integer,
    species_id integer,
    "position" integer,
    wt_residue text,
    variant_residue text,
    edit_distance integer,
    mutation_type_id integer,
    eve_score double precision,
    eve_class_75_set text,
    clinvar_label text,
    alphamissense_pathogenicity double precision,
    alphamissense_class text,
    alphafold_conf_type text
);


ALTER TABLE public.mutation OWNER TO polina;

--
-- Name: mutation_mutation_id_seq; Type: SEQUENCE; Schema: public; Owner: polina
--

CREATE SEQUENCE public.mutation_mutation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mutation_mutation_id_seq OWNER TO polina;

--
-- Name: mutation_mutation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: polina
--

ALTER SEQUENCE public.mutation_mutation_id_seq OWNED BY public.mutation.id;


--
-- Name: mutation_type; Type: TABLE; Schema: public; Owner: polina
--

CREATE TABLE public.mutation_type (
    id integer NOT NULL,
    type character varying(50) NOT NULL
);


ALTER TABLE public.mutation_type OWNER TO polina;

--
-- Name: mutation_type_mutation_type_id_seq; Type: SEQUENCE; Schema: public; Owner: polina
--

CREATE SEQUENCE public.mutation_type_mutation_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mutation_type_mutation_type_id_seq OWNER TO polina;

--
-- Name: mutation_type_mutation_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: polina
--

ALTER SEQUENCE public.mutation_type_mutation_type_id_seq OWNED BY public.mutation_type.id;


--
-- Name: species; Type: TABLE; Schema: public; Owner: polina
--

CREATE TABLE public.species (
    id integer NOT NULL,
    species_name text
);


ALTER TABLE public.species OWNER TO polina;

--
-- Name: species_species_id_seq; Type: SEQUENCE; Schema: public; Owner: polina
--

CREATE SEQUENCE public.species_species_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.species_species_id_seq OWNER TO polina;

--
-- Name: species_species_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: polina
--

ALTER SEQUENCE public.species_species_id_seq OWNED BY public.species.id;


--
-- Name: substitution_matrix; Type: TABLE; Schema: public; Owner: polina
--

CREATE TABLE public.substitution_matrix (
    amino_acid_x text NOT NULL,
    amino_acid_y text NOT NULL,
    benner22 double precision,
    benner6 double precision,
    benner74 double precision,
    blastn double precision,
    blastp double precision,
    blosum45 double precision,
    blosum50 double precision,
    blosum62 double precision,
    blosum80 double precision,
    blosum90 double precision,
    dayhoff double precision,
    feng double precision,
    genetic double precision,
    gonnet1992 double precision,
    johnson double precision,
    jones double precision,
    levin double precision,
    mclachlan double precision,
    mdm78 double precision,
    megablast double precision,
    nuc_4_4 double precision,
    pam250 double precision,
    pam30 double precision,
    pam70 double precision,
    rao double precision,
    risler double precision,
    str double precision,
    blosum62_minmax_scaled text,
    pam250_minmax_scaled text,
    grantham double precision,
    blosum100 double precision
);


ALTER TABLE public.substitution_matrix OWNER TO polina;

--
-- Name: amino_acid_property id; Type: DEFAULT; Schema: public; Owner: polina_py
--

ALTER TABLE ONLY public.amino_acid_property ALTER COLUMN id SET DEFAULT nextval('public.amino_acid_property_id_seq'::regclass);


--
-- Name: assay id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assay ALTER COLUMN id SET DEFAULT nextval('public.assay_id_seq'::regclass);


--
-- Name: dms id; Type: DEFAULT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.dms ALTER COLUMN id SET DEFAULT nextval('public.dms_dms_id_seq'::regclass);


--
-- Name: dms_range id; Type: DEFAULT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.dms_range ALTER COLUMN id SET DEFAULT nextval('public.dms_range_dms_range_id_seq'::regclass);


--
-- Name: esm1v_embeddings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.esm1v_embeddings ALTER COLUMN id SET DEFAULT nextval('public.esm1v_embeddings_id_seq'::regclass);


--
-- Name: gene_urn id; Type: DEFAULT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.gene_urn ALTER COLUMN id SET DEFAULT nextval('public.gene_urn_gene_urn_id_seq'::regclass);


--
-- Name: msa id; Type: DEFAULT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.msa ALTER COLUMN id SET DEFAULT nextval('public.msa_msa_id_seq'::regclass);


--
-- Name: mutation id; Type: DEFAULT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.mutation ALTER COLUMN id SET DEFAULT nextval('public.mutation_mutation_id_seq'::regclass);


--
-- Name: mutation_type id; Type: DEFAULT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.mutation_type ALTER COLUMN id SET DEFAULT nextval('public.mutation_type_mutation_type_id_seq'::regclass);


--
-- Name: species id; Type: DEFAULT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.species ALTER COLUMN id SET DEFAULT nextval('public.species_species_id_seq'::regclass);


--
-- Name: amino_acid_property amino_acid_property_one_letter_code_key; Type: CONSTRAINT; Schema: public; Owner: polina_py
--

ALTER TABLE ONLY public.amino_acid_property
    ADD CONSTRAINT amino_acid_property_one_letter_code_key UNIQUE (one_letter_code);


--
-- Name: amino_acid_property amino_acid_property_pkey; Type: CONSTRAINT; Schema: public; Owner: polina_py
--

ALTER TABLE ONLY public.amino_acid_property
    ADD CONSTRAINT amino_acid_property_pkey PRIMARY KEY (id);


--
-- Name: amino_acid_property amino_acid_property_three_letter_code_key; Type: CONSTRAINT; Schema: public; Owner: polina_py
--

ALTER TABLE ONLY public.amino_acid_property
    ADD CONSTRAINT amino_acid_property_three_letter_code_key UNIQUE (three_letter_code);


--
-- Name: assay assay_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assay
    ADD CONSTRAINT assay_pkey PRIMARY KEY (id);


--
-- Name: dms dms_pkey; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.dms
    ADD CONSTRAINT dms_pkey PRIMARY KEY (id);


--
-- Name: dms_range dms_range_gene_urn_id_unique; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.dms_range
    ADD CONSTRAINT dms_range_gene_urn_id_unique UNIQUE (gene_urn_id);


--
-- Name: dms_range dms_range_pkey; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.dms_range
    ADD CONSTRAINT dms_range_pkey PRIMARY KEY (id);


--
-- Name: esm1v_embeddings esm1v_embeddings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.esm1v_embeddings
    ADD CONSTRAINT esm1v_embeddings_pkey PRIMARY KEY (id);


--
-- Name: gene_urn gene_urn_pkey; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.gene_urn
    ADD CONSTRAINT gene_urn_pkey PRIMARY KEY (id);


--
-- Name: gene_urn gene_urn_urn_mavedb_key; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.gene_urn
    ADD CONSTRAINT gene_urn_urn_mavedb_key UNIQUE (urn_mavedb);


--
-- Name: msa msa_pkey; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.msa
    ADD CONSTRAINT msa_pkey PRIMARY KEY (id);


--
-- Name: mutation mutation_pkey; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.mutation
    ADD CONSTRAINT mutation_pkey PRIMARY KEY (id);


--
-- Name: mutation_type mutation_type_pkey; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.mutation_type
    ADD CONSTRAINT mutation_type_pkey PRIMARY KEY (id);


--
-- Name: mutation_type mutation_type_type_key; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.mutation_type
    ADD CONSTRAINT mutation_type_type_key UNIQUE (type);


--
-- Name: species species_pkey; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.species
    ADD CONSTRAINT species_pkey PRIMARY KEY (id);


--
-- Name: species species_species_name_key; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.species
    ADD CONSTRAINT species_species_name_key UNIQUE (species_name);


--
-- Name: substitution_matrix substitution_matrix_pkey; Type: CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.substitution_matrix
    ADD CONSTRAINT substitution_matrix_pkey PRIMARY KEY (amino_acid_x, amino_acid_y);


--
-- Name: esm1v_embeddings unique_mutation_type; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.esm1v_embeddings
    ADD CONSTRAINT unique_mutation_type UNIQUE (mutation_id, embedding_type);


--
-- Name: esm1v_embeddings esm1v_embeddings_mutation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.esm1v_embeddings
    ADD CONSTRAINT esm1v_embeddings_mutation_id_fkey FOREIGN KEY (mutation_id) REFERENCES public.mutation(id);


--
-- Name: dms fk_dms_range; Type: FK CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.dms
    ADD CONSTRAINT fk_dms_range FOREIGN KEY (dms_range_id) REFERENCES public.dms_range(id);


--
-- Name: mutation fk_gene_urn; Type: FK CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.mutation
    ADD CONSTRAINT fk_gene_urn FOREIGN KEY (gene_urn_id) REFERENCES public.gene_urn(id);


--
-- Name: dms_range fk_gene_urn; Type: FK CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.dms_range
    ADD CONSTRAINT fk_gene_urn FOREIGN KEY (gene_urn_id) REFERENCES public.gene_urn(id);


--
-- Name: dms fk_mutation; Type: FK CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.dms
    ADD CONSTRAINT fk_mutation FOREIGN KEY (mutation_id) REFERENCES public.mutation(id);


--
-- Name: msa fk_mutation; Type: FK CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.msa
    ADD CONSTRAINT fk_mutation FOREIGN KEY (mutation_id) REFERENCES public.mutation(id);


--
-- Name: mutation fk_mutation_type; Type: FK CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.mutation
    ADD CONSTRAINT fk_mutation_type FOREIGN KEY (mutation_type_id) REFERENCES public.mutation_type(id);


--
-- Name: mutation fk_species; Type: FK CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.mutation
    ADD CONSTRAINT fk_species FOREIGN KEY (species_id) REFERENCES public.species(id);


--
-- Name: gene_urn gene_urn_assay_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: polina
--

ALTER TABLE ONLY public.gene_urn
    ADD CONSTRAINT gene_urn_assay_type_fkey FOREIGN KEY (assay_type) REFERENCES public.assay(id);


--
-- Name: TABLE amino_acid_property; Type: ACL; Schema: public; Owner: polina_py
--

GRANT ALL ON TABLE public.amino_acid_property TO polina;


--
-- Name: SEQUENCE amino_acid_property_id_seq; Type: ACL; Schema: public; Owner: polina_py
--

GRANT ALL ON SEQUENCE public.amino_acid_property_id_seq TO polina;


--
-- Name: TABLE assay; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.assay TO polina;
GRANT ALL ON TABLE public.assay TO polina_py;


--
-- Name: SEQUENCE assay_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.assay_id_seq TO polina;
GRANT ALL ON SEQUENCE public.assay_id_seq TO polina_py;


--
-- Name: TABLE dms; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON TABLE public.dms TO polina_py;


--
-- Name: SEQUENCE dms_dms_id_seq; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON SEQUENCE public.dms_dms_id_seq TO polina_py;


--
-- Name: TABLE dms_range; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON TABLE public.dms_range TO polina_py;


--
-- Name: SEQUENCE dms_range_dms_range_id_seq; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON SEQUENCE public.dms_range_dms_range_id_seq TO polina_py;


--
-- Name: TABLE esm1v_embeddings; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.esm1v_embeddings TO polina;
GRANT ALL ON TABLE public.esm1v_embeddings TO polina_py;


--
-- Name: SEQUENCE esm1v_embeddings_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.esm1v_embeddings_id_seq TO polina;
GRANT ALL ON SEQUENCE public.esm1v_embeddings_id_seq TO polina_py;


--
-- Name: TABLE gene_urn; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON TABLE public.gene_urn TO polina_py;


--
-- Name: SEQUENCE gene_urn_gene_urn_id_seq; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON SEQUENCE public.gene_urn_gene_urn_id_seq TO polina_py;


--
-- Name: TABLE msa; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON TABLE public.msa TO polina_py;


--
-- Name: SEQUENCE msa_msa_id_seq; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON SEQUENCE public.msa_msa_id_seq TO polina_py;


--
-- Name: TABLE mutation; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON TABLE public.mutation TO polina_py;


--
-- Name: SEQUENCE mutation_mutation_id_seq; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON SEQUENCE public.mutation_mutation_id_seq TO polina_py;


--
-- Name: TABLE mutation_type; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON TABLE public.mutation_type TO polina_py;


--
-- Name: SEQUENCE mutation_type_mutation_type_id_seq; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON SEQUENCE public.mutation_type_mutation_type_id_seq TO polina_py;


--
-- Name: TABLE species; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON TABLE public.species TO polina_py;


--
-- Name: SEQUENCE species_species_id_seq; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON SEQUENCE public.species_species_id_seq TO polina_py;


--
-- Name: TABLE substitution_matrix; Type: ACL; Schema: public; Owner: polina
--

GRANT ALL ON TABLE public.substitution_matrix TO polina_py;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: polina
--

ALTER DEFAULT PRIVILEGES FOR ROLE polina IN SCHEMA public GRANT ALL ON SEQUENCES  TO polina;
ALTER DEFAULT PRIVILEGES FOR ROLE polina IN SCHEMA public GRANT ALL ON SEQUENCES  TO polina_py;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: polina
--

ALTER DEFAULT PRIVILEGES FOR ROLE polina IN SCHEMA public GRANT ALL ON TABLES  TO polina;
ALTER DEFAULT PRIVILEGES FOR ROLE polina IN SCHEMA public GRANT ALL ON TABLES  TO polina_py;


--
-- PostgreSQL database dump complete
--

