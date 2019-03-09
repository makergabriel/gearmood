-- DB setup
-- Install postgreSQL
-- sudo -u postgres psql
-- create database gearmood
-- create user gearmood_app with encrypted password 'gearmood_app';
-- grant all privileges on database gearmood to gearmood_app;


CREATE TABLE public.shake (
	submission_id varchar(50) NOT NULL,
	subreddit_id varchar(50) NULL,
	title varchar(300) NULL,
	"data" jsonb NULL,
	created_dt timestamp NULL,
	modified_dt timestamp NULL,
	CONSTRAINT shake_pkey PRIMARY KEY (submission_id)
);

-- Permissions

ALTER TABLE public.shake OWNER TO gearmood_app;
GRANT ALL ON TABLE public.shake TO gearmood_app;


-- Drop table

-- DROP TABLE public.cut_sentence

CREATE TABLE public.cut_sentence (
	submission_id varchar(50) NULL,
	words jsonb NULL, -- json structure of the cut, keep, change words used to recognize the gear mood.
	sentence text NULL,
	"type" varchar NULL, -- Describes if the sentence indicates to remove, add, change, or not applicable to mood.
	item varchar NULL -- The item in the sentence to change.
);

-- Column comments

COMMENT ON COLUMN public.cut_sentence.words IS 'json structure of the cut, keep, change words used to recognize the gear mood.';
COMMENT ON COLUMN public.cut_sentence."type" IS 'Describes if the sentence indicates to remove, add, change, or not applicable to mood.';
COMMENT ON COLUMN public.cut_sentence.item IS 'The item in the sentence to change.';

-- Permissions

ALTER TABLE public.cut_sentence OWNER TO gearmood_app;
GRANT ALL ON TABLE public.cut_sentence TO gearmood_app;
