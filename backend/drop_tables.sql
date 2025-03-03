SELECT 'DROP TABLE IF EXISTS ' || table_schema || '.' || table_name || ' CASCADE;' 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE';
