-- Revert sqitch:articles from pg

BEGIN;

DROP TABLE IF EXISTS public.articles;
DROP SEQUENCE IF EXISTS public.articles_id_seq;

COMMIT;
