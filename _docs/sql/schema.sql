--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: budget_category_id; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE budget_category_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_category_id OWNER TO accounts;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: budget_category; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE budget_category (
    budget_category_id integer DEFAULT nextval('budget_category_id'::regclass) NOT NULL,
    budget_category text,
    budget_amount numeric(7,2),
    budget_type_id smallint NOT NULL
);


ALTER TABLE public.budget_category OWNER TO accounts;

--
-- Name: budget_type; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE budget_type (
    budget_type_id smallint NOT NULL,
    budget_type character varying(15) NOT NULL,
    ordering smallint NOT NULL
);


ALTER TABLE public.budget_type OWNER TO accounts;

--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO accounts;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO accounts;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: qif_parser; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE qif_parser (
    id integer NOT NULL,
    parse_status text,
    date_added date NOT NULL
);


ALTER TABLE public.qif_parser OWNER TO accounts;

--
-- Name: qif_parser_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE qif_parser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qif_parser_id_seq OWNER TO accounts;

--
-- Name: qif_parser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE qif_parser_id_seq OWNED BY qif_parser.id;


--
-- Name: transaction_id; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE transaction_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_id OWNER TO accounts;

--
-- Name: transaction; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE transaction (
    transaction_id integer DEFAULT nextval('transaction_id'::regclass) NOT NULL,
    transaction_date date
);


ALTER TABLE public.transaction OWNER TO accounts;

--
-- Name: transaction_category_id; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE transaction_category_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_category_id OWNER TO accounts;

--
-- Name: transaction_category; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE transaction_category (
    transaction_category_id integer DEFAULT nextval('transaction_category_id'::regclass) NOT NULL,
    transaction_category_parent_id integer,
    budget_category_id integer,
    transaction_category text
);


ALTER TABLE public.transaction_category OWNER TO accounts;

--
-- Name: transaction_line_id; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE transaction_line_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_line_id OWNER TO accounts;

--
-- Name: transaction_line; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE transaction_line (
    transaction_line_id integer DEFAULT nextval('transaction_line_id'::regclass) NOT NULL,
    transaction_id integer,
    transaction_category_id integer,
    amount numeric(9,2)
);


ALTER TABLE public.transaction_line OWNER TO accounts;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY qif_parser ALTER COLUMN id SET DEFAULT nextval('qif_parser_id_seq'::regclass);


--
-- Name: budget_category_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY budget_category
    ADD CONSTRAINT budget_category_pkey PRIMARY KEY (budget_category_id);


--
-- Name: budget_type_ordering_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY budget_type
    ADD CONSTRAINT budget_type_ordering_key UNIQUE (ordering);


--
-- Name: budget_type_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY budget_type
    ADD CONSTRAINT budget_type_pkey PRIMARY KEY (budget_type_id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: qif_parser_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY qif_parser
    ADD CONSTRAINT qif_parser_pkey PRIMARY KEY (id);


--
-- Name: transaction_category_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY transaction_category
    ADD CONSTRAINT transaction_category_pkey PRIMARY KEY (transaction_category_id);


--
-- Name: transaction_line_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY transaction_line
    ADD CONSTRAINT transaction_line_pkey PRIMARY KEY (transaction_line_id);


--
-- Name: transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (transaction_id);


--
-- Name: budget_category_budget_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget_category
    ADD CONSTRAINT budget_category_budget_type_id_fkey FOREIGN KEY (budget_type_id) REFERENCES budget_type(budget_type_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: transaction_category_transaction_category_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY transaction_category
    ADD CONSTRAINT transaction_category_transaction_category_parent_id_fkey FOREIGN KEY (transaction_category_parent_id) REFERENCES transaction_category(transaction_category_id);


--
-- Name: transaction_line_transaction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY transaction_line
    ADD CONSTRAINT transaction_line_transaction_id_fkey FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

