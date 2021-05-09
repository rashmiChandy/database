import logging

from businessLogic import InsertQuery, DeleteQuery
from businessLogic.CreateValidation import CreateValidation
from businessLogic.SelectSqlValidation import SelectSqlValidation
from businessLogic.UpdateValidation import UpdateSqlValidation
from businessLogic.methods import executeQueries

global database
database = ""


def parseQuery():
    queryCreateDb = [{
        'query': 'create database',
        'databaseName': 'sampledb'
    }
    ]

    queryUse = [{
        'query': 'use',
        'databaseName': 'sampledb'
    }
    ]

    querySelect = [{
        'query': 'select',
        'tableName': 'orders',
        'attributeN': ['*'],
        'whereAttribute': 'FALSE',
        'whereVariable': 'FALSE'
    }
    ]
    querySelect2 = [{
        'query': 'select',
        'tableName': 'orders',
        'attributeN': ['*'],
        'whereAttribute': 'orderNumber',
        'whereVariable': 100
    }
    ]

    querySelect3 = [{
        'query': 'select',
        'tableName': 'orders',
        'attributeN': ['orderNumber', 'shippedDate', 'customerNumber'],
        'whereAttribute': 'orderNumber',
        'whereVariable': 100
    }
    ]

    queryInsert = [{
        'query': 'insert',
        'tableName': 'customers',
        'attributeN': ['customerNumber', 'customerName', 'customerLastName', 'city', 'postalCode'],
        'values': [2, 'Kevin', 'Kwan', 'Ontario', 'B3H 4R2']
    }
    ]
    queryInsert1 = [{
        'query': 'insert',
        'tableName': 'customers',
        'attributeN': ['orderNumber', 'orderLocation', 'orderArea', 'status', 'customerNumber'],
        'values': [2, 'Halifax', 'Nova Scotia', 'inprogress', 1]
    }
    ]

    queryUpdate = [{
        'query': 'update',
        'tableName': 'customers',
        'attributeN': ['customerNumber', 'customerName', 'customerLastName', 'city', 'postalCode'],
        'whereAttribute': 'customerName',
        'whereVariable': 'Amelia'
    }
    ]

    queryDelete = [{
        'query': 'delete',
        'tableName': 'customers',
        'whereAttribute': 'customerName',
        'whereVariable': 'Amelia'
    }
    ]

    queryCreate = [{
        'query': 'create',
        'tableName': 'orders',
        'attributeN': 'orderNumber',
        'dataType': 'INT',
        'primaryKey': 'TRUE',
        'foreignKey': 'FALSE',
        'relationshipTable': 'FALSE',
        'relationshipAttribute': 'FALSE'
    },
        {'query': 'create',
         'tableName': 'orders',
         'attributeN': 'orderDate',
         'dataType': 'VARCHAR',
         'primaryKey': 'FALSE',
         'foreignKey': 'FALSE',
         'relationshipTable': 'FALSE',
         'relationshipAttribute': 'FALSE'
         },
        {'query': 'create',
         'tableName': 'orders',
         'attributeN': 'shippedDate',
         'dataType': 'VARCHAR',
         'primaryKey': 'FALSE',
         'foreignKey': 'FALSE',
         'relationshipTable': 'FALSE',
         'relationshipAttribute': 'FALSE'
         },
        {'query': 'create',
         'tableName': 'orders',
         'attributeN': 'status',
         'dataType': 'VARCHAR',
         'primaryKey': 'FALSE',
         'foreignKey': 'FALSE',
         'relationshipTable': 'FALSE',
         'relationshipAttribute': 'FALSE'
         },
        {'query': 'create',
         'tableName': 'orders',
         'attributeN': 'customerNumber',
         'dataType': 'INT',
         'primaryKey': 'FALSE',
         'foreignKey': 'TRUE',
         'relationshipTable': 'customers',
         'relationshipAttribute': 'customerNumber'
         }
    ]

    querySqlDump = [{
        'query': 'mysqldump',
        'pathAndFilename': '/home/amelia/sqlDumps'  # sqlDumps is the filename without extension
    }
    ]

    queryErd = [{
        'query': 'export erd',
        'pathAndFilename': '/home/amelia/erd'  # erd is the filename without extension
    }
    ]

    # interpretQuery(queryCreateDb)
    interpretQuery(queryUse)
    # interpretQuery(querySelect3)
    # interpretQuery(queryCreate)
    # interpretQuery(querySqlDump)
    interpretQuery(queryErd)


def interpretQuery(query, complete_query):
    global database
    queryType = query[0]['query']
    create_validation = CreateValidation
    select_sql_validation = SelectSqlValidation
    update_sql_validation = UpdateSqlValidation

    if queryType == 'create database':
        print("---The query is create database---")
        create_dictionary = create_validation.validate_parse_create_db(create_validation, complete_query)
        databaseName = create_dictionary[0]['databaseName']
        if create_dictionary:
            code = executeQueries.createDbQuery(databaseName)
            if code == 0:
                print("The database", databaseName, "already exists")
            elif code == 1:
                print("Database", databaseName, "created")

    elif queryType == 'use':
        print("---The query is use---")
        use_dictionary = create_validation.validate_parse_use_db(create_validation, complete_query)
        databaseName = use_dictionary[0]['databaseName']
        if use_dictionary:
            code = executeQueries.useQuery(databaseName)
            if code == 0:
                database = databaseName
                print("Use", database)
            elif code == 1:
                print("Error the database", databaseName, "does not exist")

    elif queryType == 'create':
        print("---The query is create---")
        create_dictionary = create_validation.validate_parse_create_query(create_validation, complete_query)
        if create_dictionary:
            code = executeQueries.createQuery(database, create_dictionary)
            if code == 0:
                print('Database is not selected, Use a database')
            elif code == 1:
                print("Table already exists")
            elif code == 2:
                print("Cannot create table: a foreign table or attribute does not exist")
            elif code == 3:
                print("Table created")
            elif code == 4:
                print("An error ocurred")

    elif queryType == 'select':
        print("---The query is select---")
        select_dictionary = select_sql_validation.validate_parse_select(select_sql_validation, complete_query)
        if select_dictionary:
            code = executeQueries.selectQuery(database, select_dictionary)
            if code == 0:
                print("Database not selected")
            elif code[0] == 1:
                print(code[1])
            elif code == 2:
                print("Table does not exist")
            elif code == 3:
                print("An error ocurred")

    elif queryType == 'insert':
        print("---The query is insert---")
        insert_dictionary = InsertQuery.insert_query(complete_query)
        if insert_dictionary:
            code = executeQueries.insertQuery(database, insert_dictionary)

    elif queryType == 'update':
        print("---The query is update---")
        update_dictionary = update_sql_validation.validate_parse_update(update_sql_validation, complete_query)
        if update_dictionary:
            code = executeQueries.updateQuery(database, update_dictionary)

    elif queryType == 'delete':
        print("---The query is delete---")
        code = 0
        delete_dictionary = DeleteQuery.delete_query(complete_query)  # Validate query
        if delete_dictionary:
            code = executeQueries.deleteQuery(database, delete_dictionary)
            if code == 0:
                print("Database not selected")

    elif queryType == 'mysqldump':
        print("---The query is mysqldump---")
        code = executeQueries.mysqldumpQuery(database, query)
        if code == 0:
            print("Database not selected")
        elif code == 1:
            print("Sql dump generated")
        elif code == 2:
            print("An error ocurred")

    elif queryType == 'export erd':
        print("---The query is export erd---")
        code = executeQueries.exporterdQuery(database, query)
        if code == 0:
            print("Database not selected")
        elif code == 1:
            print("ERD generated")
        elif code == 2:
            print("An error ocurred")
    elif queryType == 'logout':
        print('User logout!')


def sample_main():
    logger = logging.getLogger('example_logger')
    logging.basicConfig(filename='5408_G10_.log', filemode='a',
                        format='%(asctime)s - [%(process)d] - %(levelname)s - %(message)s', level=logging.DEBUG)
    logging.info('!!************* DATABASE & DATABASE MANAGEMENT SYSTEM *************!!')

    insert_query = "INSERT INTO table_name (column1, column2, column3) VALUES (value1, value2, value3);"
    InsertQuery.insert_query(insert_query)
    delete_query = "DELETE FROM payments WHERE customerNumber = 1;"
    DeleteQuery.delete_query(delete_query)

    # parseQuery()


'''
----------------
|SAMPLE QUERIES|
----------------
CREATE DATABASE sampledb;

CREATE TABLE orders (
  orderNumber int,
  orderDate varchar,
  shippedDate varchar,
  status varchar,
  customerNumber int,
  PRIMARY KEY (orderNumber),
  FOREIGN KEY (customerNumber) REFERENCES customers (customerNumber)
);

SELECT * from customers;
SELECT customerNumber, customerName, customerLastName, city, postalCode from customers;
SELECT customerNumber, customerName, customerLastName, city, postalCode from customers 
where customerName = 'Amelia';

INSERT into customers(customerNumber, customerName, customerLastName, city, postalCode)
values(2, 'Kevin','Kwan','Ontario', 'B3H 4R2' );

UPDATE customers SET customerName = 'Diana'
WHERE customerNumber = 1

DELETE FROM payments WHERE customerNumber = 1;

mysqldump -u YourUser -p YourDatabaseName > /home/amelia/sqlDumps
mysqldump > /home/amelia/sqlDumps

export erd; # I did not find the command to create the ERD

'''
