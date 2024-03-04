--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

-- Started on 2024-03-04 09:41:22

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
-- TOC entry 214 (class 1259 OID 16718)
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id_cat integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16744)
-- Name: document_terms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_terms (
    doc_number integer NOT NULL,
    term text NOT NULL,
    term_count integer NOT NULL
);


ALTER TABLE public.document_terms OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16725)
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    doc_number integer NOT NULL,
    doc_text text NOT NULL,
    doc_title text NOT NULL,
    doc_date date NOT NULL,
    num_chars integer NOT NULL,
    id_cat integer NOT NULL
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16737)
-- Name: terms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.terms (
    term text NOT NULL,
    num_chars integer NOT NULL
);


ALTER TABLE public.terms OWNER TO postgres;

--
-- TOC entry 3185 (class 2606 OID 16724)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id_cat);


--
-- TOC entry 3191 (class 2606 OID 16750)
-- Name: document_terms document_terms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_terms
    ADD CONSTRAINT document_terms_pkey PRIMARY KEY (term, doc_number);


--
-- TOC entry 3187 (class 2606 OID 16731)
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (doc_number);


--
-- TOC entry 3189 (class 2606 OID 16743)
-- Name: terms term_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.terms
    ADD CONSTRAINT term_pkey PRIMARY KEY (term);


--
-- TOC entry 3193 (class 2606 OID 16751)
-- Name: document_terms fk_doc_number; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_terms
    ADD CONSTRAINT fk_doc_number FOREIGN KEY (doc_number) REFERENCES public.documents(doc_number) NOT VALID;


--
-- TOC entry 3192 (class 2606 OID 16732)
-- Name: documents fk_id_cat; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT fk_id_cat FOREIGN KEY (id_cat) REFERENCES public.categories(id_cat) NOT VALID;


--
-- TOC entry 3194 (class 2606 OID 16756)
-- Name: document_terms fk_term; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_terms
    ADD CONSTRAINT fk_term FOREIGN KEY (term) REFERENCES public.terms(term) NOT VALID;


-- Completed on 2024-03-04 09:41:23

--
-- PostgreSQL database dump complete
--

