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

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO accounts;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO accounts;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO accounts;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO accounts;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO accounts;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO accounts;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO accounts;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO accounts;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO accounts;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO accounts;

--
-- Name: auth_user_id_seq1; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_user_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq1 OWNER TO accounts;

--
-- Name: auth_user_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_user_id_seq1 OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO accounts;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO accounts;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: budget; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE budget (
    budget_id integer NOT NULL,
    budget_name text NOT NULL,
    budget_description text NOT NULL,
    budget_master boolean NOT NULL
);


ALTER TABLE public.budget OWNER TO accounts;

--
-- Name: budget_amount; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE budget_amount (
    budget_amount_id integer NOT NULL,
    budget_amount numeric(7,2),
    start_date date NOT NULL,
    end_date date,
    budget_id integer,
    budget_category_id integer
);


ALTER TABLE public.budget_amount OWNER TO accounts;

--
-- Name: budget_amount_budget_amount_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE budget_amount_budget_amount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_amount_budget_amount_id_seq OWNER TO accounts;

--
-- Name: budget_amount_budget_amount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE budget_amount_budget_amount_id_seq OWNED BY budget_amount.budget_amount_id;


--
-- Name: budget_budget_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE budget_budget_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_budget_id_seq OWNER TO accounts;

--
-- Name: budget_budget_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE budget_budget_id_seq OWNED BY budget.budget_id;


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

--
-- Name: budget_category; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE budget_category (
    budget_category_id integer DEFAULT nextval('budget_category_id'::regclass) NOT NULL,
    budget_category text,
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
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO accounts;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO accounts;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO accounts;

--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer DEFAULT nextval('django_content_type_id_seq'::regclass) NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO accounts;

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
-- Name: django_session; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO accounts;

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
-- Name: qif_parser; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE qif_parser (
    id integer DEFAULT nextval('qif_parser_id_seq'::regclass) NOT NULL,
    parse_status text,
    date_added date NOT NULL
);


ALTER TABLE public.qif_parser OWNER TO accounts;

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

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq1'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: budget_id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget ALTER COLUMN budget_id SET DEFAULT nextval('budget_budget_id_seq'::regclass);


--
-- Name: budget_amount_id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget_amount ALTER COLUMN budget_amount_id SET DEFAULT nextval('budget_amount_budget_amount_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey1; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey1 PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key1; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key1 UNIQUE (username);


--
-- Name: budget_amount_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY budget_amount
    ADD CONSTRAINT budget_amount_pkey PRIMARY KEY (budget_amount_id);


--
-- Name: budget_category_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY budget_category
    ADD CONSTRAINT budget_category_pkey PRIMARY KEY (budget_category_id);


--
-- Name: budget_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY budget
    ADD CONSTRAINT budget_pkey PRIMARY KEY (budget_id);


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
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_45f3b1d93ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_45f3b1d93ec8c61c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


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
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: budget_amount_7748a592; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX budget_amount_7748a592 ON budget_amount USING btree (budget_id);


--
-- Name: budget_amount_90a63c7c; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX budget_amount_90a63c7c ON budget_amount USING btree (budget_category_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_like; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX django_session_session_key_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: D3a8426412148d1e982adbbf5c808e03; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget_amount
    ADD CONSTRAINT "D3a8426412148d1e982adbbf5c808e03" FOREIGN KEY (budget_category_id) REFERENCES budget_category(budget_category_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_content_type_id_508cf46651277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_508cf46651277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: budget_amount_budget_id_3f19ce1f52908e8_fk_budget_budget_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget_amount
    ADD CONSTRAINT budget_amount_budget_id_3f19ce1f52908e8_fk_budget_budget_id FOREIGN KEY (budget_id) REFERENCES budget(budget_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: budget_category_budget_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget_category
    ADD CONSTRAINT budget_category_budget_type_id_fkey FOREIGN KEY (budget_type_id) REFERENCES budget_type(budget_type_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: djan_content_type_id_697914295151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_697914295151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


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

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
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

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE account (
    account_id integer NOT NULL,
    account_name text NOT NULL,
    account_notes text,
    account_type_id integer,
    account_hidden boolean NOT NULL
);


ALTER TABLE public.account OWNER TO accounts;

--
-- Name: account_type; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE account_type (
    account_type_id integer NOT NULL,
    account_type text NOT NULL,
    ordering integer NOT NULL,
    CONSTRAINT account_type_ordering_check CHECK ((ordering >= 0))
);


ALTER TABLE public.account_type OWNER TO accounts;

--
-- Name: account_type_account_type_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE account_type_account_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_type_account_type_id_seq OWNER TO accounts;

--
-- Name: account_type_account_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE account_type_account_type_id_seq OWNED BY account_type.account_type_id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO accounts;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO accounts;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO accounts;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO accounts;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO accounts;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO accounts;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO accounts;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO accounts;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO accounts;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO accounts;

--
-- Name: auth_user_id_seq1; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_user_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq1 OWNER TO accounts;

--
-- Name: auth_user_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_user_id_seq1 OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO accounts;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO accounts;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: budget; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE budget (
    budget_id integer NOT NULL,
    budget_name text NOT NULL,
    budget_description text NOT NULL,
    budget_master boolean NOT NULL
);


ALTER TABLE public.budget OWNER TO accounts;

--
-- Name: budget_amount; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE budget_amount (
    budget_amount_id integer NOT NULL,
    budget_amount numeric(7,2),
    start_date date NOT NULL,
    end_date date,
    budget_id integer,
    budget_category_id integer
);


ALTER TABLE public.budget_amount OWNER TO accounts;

--
-- Name: budget_amount_budget_amount_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE budget_amount_budget_amount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_amount_budget_amount_id_seq OWNER TO accounts;

--
-- Name: budget_amount_budget_amount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE budget_amount_budget_amount_id_seq OWNED BY budget_amount.budget_amount_id;


--
-- Name: budget_budget_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE budget_budget_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_budget_id_seq OWNER TO accounts;

--
-- Name: budget_budget_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE budget_budget_id_seq OWNED BY budget.budget_id;


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

--
-- Name: budget_category; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE budget_category (
    budget_category_id integer DEFAULT nextval('budget_category_id'::regclass) NOT NULL,
    budget_category text,
    budget_type_id smallint
);


ALTER TABLE public.budget_category OWNER TO accounts;

--
-- Name: budget_type; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE budget_type (
    budget_type_id smallint NOT NULL,
    budget_type text NOT NULL,
    ordering smallint NOT NULL
);


ALTER TABLE public.budget_type OWNER TO accounts;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO accounts;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO accounts;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO accounts;

--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer DEFAULT nextval('django_content_type_id_seq'::regclass) NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO accounts;

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
-- Name: django_session; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO accounts;

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
-- Name: qif_parser; Type: TABLE; Schema: public; Owner: accounts; Tablespace: 
--

CREATE TABLE qif_parser (
    id integer DEFAULT nextval('qif_parser_id_seq'::regclass) NOT NULL,
    parse_status text,
    date_added date NOT NULL
);


ALTER TABLE public.qif_parser OWNER TO accounts;

--
-- Name: simple_budget_account_account_id_seq; Type: SEQUENCE; Schema: public; Owner: accounts
--

CREATE SEQUENCE simple_budget_account_account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_budget_account_account_id_seq OWNER TO accounts;

--
-- Name: simple_budget_account_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: accounts
--

ALTER SEQUENCE simple_budget_account_account_id_seq OWNED BY account.account_id;


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
    transaction_date date,
    account_id integer
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
-- Name: account_id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY account ALTER COLUMN account_id SET DEFAULT nextval('simple_budget_account_account_id_seq'::regclass);


--
-- Name: account_type_id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY account_type ALTER COLUMN account_type_id SET DEFAULT nextval('account_type_account_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq1'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: budget_id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget ALTER COLUMN budget_id SET DEFAULT nextval('budget_budget_id_seq'::regclass);


--
-- Name: budget_amount_id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget_amount ALTER COLUMN budget_amount_id SET DEFAULT nextval('budget_amount_budget_amount_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: account_type_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY account_type
    ADD CONSTRAINT account_type_pkey PRIMARY KEY (account_type_id);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey1; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey1 PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key1; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key1 UNIQUE (username);


--
-- Name: budget_amount_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY budget_amount
    ADD CONSTRAINT budget_amount_pkey PRIMARY KEY (budget_amount_id);


--
-- Name: budget_category_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY budget_category
    ADD CONSTRAINT budget_category_pkey PRIMARY KEY (budget_category_id);


--
-- Name: budget_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY budget
    ADD CONSTRAINT budget_pkey PRIMARY KEY (budget_id);


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
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_45f3b1d93ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_45f3b1d93ec8c61c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: qif_parser_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY qif_parser
    ADD CONSTRAINT qif_parser_pkey PRIMARY KEY (id);


--
-- Name: simple_budget_account_pkey; Type: CONSTRAINT; Schema: public; Owner: accounts; Tablespace: 
--

ALTER TABLE ONLY account
    ADD CONSTRAINT simple_budget_account_pkey PRIMARY KEY (account_id);


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
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: budget_amount_7748a592; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX budget_amount_7748a592 ON budget_amount USING btree (budget_id);


--
-- Name: budget_amount_90a63c7c; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX budget_amount_90a63c7c ON budget_amount USING btree (budget_category_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_like; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX django_session_session_key_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: simple_budget_account_d18f477c; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX simple_budget_account_d18f477c ON account USING btree (account_type_id);


--
-- Name: transaction_8a089c2a; Type: INDEX; Schema: public; Owner: accounts; Tablespace: 
--

CREATE INDEX transaction_8a089c2a ON transaction USING btree (account_id);


--
-- Name: D38d78680061548b4f00986358fe8273; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY account
    ADD CONSTRAINT "D38d78680061548b4f00986358fe8273" FOREIGN KEY (account_type_id) REFERENCES account_type(account_type_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D3a8426412148d1e982adbbf5c808e03; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget_amount
    ADD CONSTRAINT "D3a8426412148d1e982adbbf5c808e03" FOREIGN KEY (budget_category_id) REFERENCES budget_category(budget_category_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_content_type_id_508cf46651277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_508cf46651277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: b_budget_type_id_65393ad90ee5e4fa_fk_budget_type_budget_type_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget_category
    ADD CONSTRAINT b_budget_type_id_65393ad90ee5e4fa_fk_budget_type_budget_type_id FOREIGN KEY (budget_type_id) REFERENCES budget_type(budget_type_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: budget_amount_budget_id_3f19ce1f52908e8_fk_budget_budget_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY budget_amount
    ADD CONSTRAINT budget_amount_budget_id_3f19ce1f52908e8_fk_budget_budget_id FOREIGN KEY (budget_id) REFERENCES budget(budget_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djan_content_type_id_697914295151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_697914295151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transaction_account_id_dda320160b69401_fk_account_account_id; Type: FK CONSTRAINT; Schema: public; Owner: accounts
--

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_account_id_dda320160b69401_fk_account_account_id FOREIGN KEY (account_id) REFERENCES account(account_id) DEFERRABLE INITIALLY DEFERRED;


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

