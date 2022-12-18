-- Deploy sqitch:articles to pg

BEGIN;

CREATE SEQUENCE IF NOT EXISTS public.articles_id_seq;

CREATE TABLE IF NOT EXISTS public.articles (
  id INTEGER NOT NULL DEFAULT NEXTVAL(
    'articles_id_seq' :: regclass
  ), 
  "title" TEXT NOT NULL, 
  "image_url" TEXT, 
  "published_date" VARCHAR(20), 
  "publisher_name" VARCHAR(255), 
  "html_content" TEXT, 
  "page_url" TEXT, 
  "category_tags" TEXT[], 
  "topic" VARCHAR(255), 
  "tags" TEXT[], 
  "source" VARCHAR(255), 
  "created_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(), 
  "updated_at" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(), 
  CONSTRAINT articles_pkey PRIMARY KEY (id)
);

CREATE OR REPLACE FUNCTION trigger_set_timestamp() RETURNS TRIGGER AS $$
BEGIN
 NEW."updated_at" = NOW();
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_set_timestamp
BEFORE UPDATE ON public.articles
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

COMMIT;

