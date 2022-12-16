-- Verify sqitch:articles on pg

BEGIN;

DO $$ BEGIN IF NOT EXISTS (
  SELECT 
    * 
  FROM 
    information_schema.tables 
  WHERE 
    table_name = 'articles'
) THEN RAISE EXCEPTION 'articles table doesn''t exit';
END IF;
END;
$$;

ROLLBACK;