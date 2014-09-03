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
  budget_amount numeric(7,2)
);


ALTER TABLE public.budget_category OWNER TO accounts;

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
  amount numeric(7,2)
);


ALTER TABLE public.transaction_line OWNER TO accounts;

--
-- Name: budget_category_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace:
--

ALTER TABLE ONLY budget_category
ADD CONSTRAINT budget_category_pkey PRIMARY KEY (budget_category_id);


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