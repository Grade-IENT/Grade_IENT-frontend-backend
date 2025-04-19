DO $$
DECLARE
    drop_stmt text;
BEGIN
    FOR drop_stmt IN 
        SELECT 'DROP TABLE IF EXISTS ' || table_schema || '.' || table_name || ' CASCADE;'
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
    LOOP
        EXECUTE drop_stmt;
    END LOOP;
END $$;
