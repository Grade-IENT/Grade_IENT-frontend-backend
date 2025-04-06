
Watch this video to install postgreSQL: https://www.youtube.com/watch?v=4qH-7w5LZsA
- Just install if you dont need to do anything on StackBuilder

1. Run 'psql -U postgres' in terminal
- if you gave a username, then use that instead of postgres
2. Put in your password
3. Create a database in the command line 
 - CREATE DATABASE gradientdb;
4. Go into that database
- \c gradientdb
5. Run the schema file to create the tables in your db
- \i {copy the path of schema.sql and put it here}
-   for windows need to make then all forward slashes to work 
6. You can use pgAdmin to play around with the db 
7. To populate the database, run the databasePopulator.py file

\dt to see the tables