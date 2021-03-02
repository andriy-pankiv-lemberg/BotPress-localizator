--
-- PostgreSQL database cluster dump
--

-- Started on 2021-03-02 22:52:08

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;






--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 11.7 (Debian 11.7-2.pgdg90+1)
-- Dumped by pg_dump version 12.1

-- Started on 2021-03-02 22:52:08

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

-- Completed on 2021-03-02 22:52:09

--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 11.7 (Debian 11.7-2.pgdg90+1)
-- Dumped by pg_dump version 12.1

-- Started on 2021-03-02 22:52:09

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

--
-- TOC entry 199 (class 1259 OID 16446)
-- Name: actions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actions (
    id bigint NOT NULL,
    title character varying NOT NULL,
    card_id bigint NOT NULL,
    phrase_id bigint NOT NULL
);


ALTER TABLE public.actions OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 16444)
-- Name: actions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.actions ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.actions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 196 (class 1259 OID 16409)
-- Name: bots; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bots (
    id bigint NOT NULL,
    lang character varying,
    file_name character varying NOT NULL
);


ALTER TABLE public.bots OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 16432)
-- Name: bots_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.bots ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.bots_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 207 (class 1259 OID 16631)
-- Name: cards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cards (
    id bigint NOT NULL,
    element_id character varying NOT NULL,
    bot_id bigint NOT NULL,
    title character varying,
    subtitle character varying,
    schema json NOT NULL,
    phrase_id bigint NOT NULL,
    lang character varying NOT NULL
);


ALTER TABLE public.cards OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16629)
-- Name: cards_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.cards ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.cards_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 201 (class 1259 OID 16501)
-- Name: choices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.choices (
    id bigint NOT NULL,
    title character varying,
    single_choice_id bigint NOT NULL,
    phrase_id bigint NOT NULL
);


ALTER TABLE public.choices OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 16499)
-- Name: choices_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.choices ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.choices_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 211 (class 1259 OID 24578)
-- Name: phrases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.phrases (
    id bigint NOT NULL,
    lang character varying NOT NULL,
    text character varying NOT NULL
);


ALTER TABLE public.phrases OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 24576)
-- Name: csv_mapper_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.phrases ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.csv_mapper_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 209 (class 1259 OID 16646)
-- Name: single_choices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.single_choices (
    id bigint NOT NULL,
    element_id character varying NOT NULL,
    bot_id bigint NOT NULL,
    text character varying,
    schema json NOT NULL,
    phrase_id bigint NOT NULL,
    lang character varying NOT NULL
);


ALTER TABLE public.single_choices OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 16644)
-- Name: single_choices_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.single_choices ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.single_choices_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 205 (class 1259 OID 16616)
-- Name: texts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.texts (
    id bigint NOT NULL,
    element_id character varying NOT NULL,
    bot_id bigint NOT NULL,
    text character varying,
    schema json NOT NULL,
    phrase_id bigint NOT NULL,
    lang character varying NOT NULL
);


ALTER TABLE public.texts OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16614)
-- Name: texts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.texts ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.texts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 203 (class 1259 OID 16556)
-- Name: variations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.variations (
    id bigint NOT NULL,
    text character varying,
    text_id bigint NOT NULL,
    phrase_id bigint NOT NULL
);


ALTER TABLE public.variations OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16554)
-- Name: variations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.variations ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.variations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 2793 (class 2606 OID 16453)
-- Name: actions actions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_pkey PRIMARY KEY (id);


--
-- TOC entry 2791 (class 2606 OID 16416)
-- Name: bots bots_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bots
    ADD CONSTRAINT bots_pkey PRIMARY KEY (id);


--
-- TOC entry 2799 (class 2606 OID 16638)
-- Name: cards cards_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cards
    ADD CONSTRAINT cards_pkey PRIMARY KEY (id);


--
-- TOC entry 2795 (class 2606 OID 16508)
-- Name: choices choices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.choices
    ADD CONSTRAINT choices_pkey PRIMARY KEY (id);


--
-- TOC entry 2803 (class 2606 OID 24585)
-- Name: phrases csv_mapper_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phrases
    ADD CONSTRAINT csv_mapper_pkey PRIMARY KEY (id);


--
-- TOC entry 2801 (class 2606 OID 16653)
-- Name: single_choices single_choices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.single_choices
    ADD CONSTRAINT single_choices_pkey PRIMARY KEY (id);


--
-- TOC entry 2797 (class 2606 OID 16623)
-- Name: texts texts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.texts
    ADD CONSTRAINT texts_pkey PRIMARY KEY (id);


--
-- TOC entry 2804 (class 2606 OID 16701)
-- Name: actions fk_action_card; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actions
    ADD CONSTRAINT fk_action_card FOREIGN KEY (card_id) REFERENCES public.cards(id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 2805 (class 2606 OID 24653)
-- Name: actions fk_action_phrase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actions
    ADD CONSTRAINT fk_action_phrase FOREIGN KEY (phrase_id) REFERENCES public.phrases(id) NOT VALID;


--
-- TOC entry 2812 (class 2606 OID 16639)
-- Name: cards fk_card_bot; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cards
    ADD CONSTRAINT fk_card_bot FOREIGN KEY (bot_id) REFERENCES public.bots(id) ON DELETE CASCADE;


--
-- TOC entry 2813 (class 2606 OID 24658)
-- Name: cards fk_card_phrase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cards
    ADD CONSTRAINT fk_card_phrase FOREIGN KEY (phrase_id) REFERENCES public.phrases(id) NOT VALID;


--
-- TOC entry 2807 (class 2606 OID 24678)
-- Name: choices fk_choice_phrase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.choices
    ADD CONSTRAINT fk_choice_phrase FOREIGN KEY (phrase_id) REFERENCES public.phrases(id) NOT VALID;


--
-- TOC entry 2806 (class 2606 OID 16696)
-- Name: choices fk_choice_single_choices; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.choices
    ADD CONSTRAINT fk_choice_single_choices FOREIGN KEY (single_choice_id) REFERENCES public.single_choices(id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 2814 (class 2606 OID 16654)
-- Name: single_choices fk_single_choice_bot; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.single_choices
    ADD CONSTRAINT fk_single_choice_bot FOREIGN KEY (bot_id) REFERENCES public.bots(id) ON DELETE CASCADE;


--
-- TOC entry 2815 (class 2606 OID 24663)
-- Name: single_choices fk_single_choice_phrase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.single_choices
    ADD CONSTRAINT fk_single_choice_phrase FOREIGN KEY (phrase_id) REFERENCES public.phrases(id) NOT VALID;


--
-- TOC entry 2810 (class 2606 OID 16624)
-- Name: texts fk_text_bot; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.texts
    ADD CONSTRAINT fk_text_bot FOREIGN KEY (bot_id) REFERENCES public.bots(id) ON DELETE CASCADE;


--
-- TOC entry 2811 (class 2606 OID 24668)
-- Name: texts fk_text_phrase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.texts
    ADD CONSTRAINT fk_text_phrase FOREIGN KEY (phrase_id) REFERENCES public.phrases(id) NOT VALID;


--
-- TOC entry 2809 (class 2606 OID 24648)
-- Name: variations fk_variation_phrase; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.variations
    ADD CONSTRAINT fk_variation_phrase FOREIGN KEY (phrase_id) REFERENCES public.phrases(id) NOT VALID;


--
-- TOC entry 2808 (class 2606 OID 24673)
-- Name: variations fk_variation_text; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.variations
    ADD CONSTRAINT fk_variation_text FOREIGN KEY (phrase_id) REFERENCES public.phrases(id) NOT VALID;


-- Completed on 2021-03-02 22:52:12

--
-- PostgreSQL database dump complete
--

-- Completed on 2021-03-02 22:52:12

--
-- PostgreSQL database cluster dump complete
--

