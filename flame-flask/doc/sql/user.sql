-- ****--------------------------------------------------------------------
-- Table: public.user
-- DROP TABLE IF EXISTS public."user";

CREATE TABLE IF NOT EXISTS public."user"
(
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    phone character varying COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    create_time timestamp with time zone NOT NULL,
    update_time timestamp with time zone,
    CONSTRAINT user_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."user"
    OWNER to postgres;

COMMENT ON TABLE public."user"
    IS '用户表';
-- --------------------------------------------------------------------****


-- ****--------------------------------------------------------------------
-- Table: public.user
-- insert example data

INSERT INTO public."user" (id, user_id, phone, password, create_time, update_time)
VALUES 
(1, 1001, '12345678901', 'password1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 1002, '12345678902', 'password2', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 1003, '12345678903', 'password3', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- --------------------------------------------------------------------****
