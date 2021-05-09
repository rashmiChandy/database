# Database
Database design and implementation from scratch that provides basic functionalities similar to MySQL.

Functionalities:
- Basic Menu with the below options 
  1. New user
  2. Existing user
  3. MySQL Command prompt
  4. MySQL Dump
  5. Export ERD
  6. Exit from application 

Application Flow:
1. Read username and password 
2. Perform verification of credentials 
3. Recover the system state for the user
4. Read the query from the user 
5. Verify if the query is valid 
6. Parse the query from the user 
7. Perform the query (select, update, insert, delete)
8. Update the logs 
9. Display a message if the operation was successful 

 
SQL queries and features which are supported in the current version:
  1. CREATE
  2. INSERT
  3. UPDATE
  4. DELETE
  5. SELECT
  6. SQL DUMP
  7. ERD generation
  8. FOREIGN KEY support

User store instructions:

- user_store.enc_copy: Empty user store with the columns : username, password

- Copy  'user_store.enc_copy' from main_module and rename it to 'user_store.enc'.

- Place 'user_store.enc' in the same location as AuthenticationMechanism.py before running the program.

- Refer PNGs for sample execution

Libraries used:
AES and Numpy
