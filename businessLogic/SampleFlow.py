from methods import executeQueries

global database
database = ""


def parseQuery():
    queryCreateDb = [{
        'query': 'create database',
        'databaseName': 'sampledb'
    }
    ]

    queryCreateDb2 = [{
        'query': 'create database',
        'databaseName': 'testdb'
    }
    ]

    queryUse = [{
        'query': 'use',
        'databaseName': 'sampledb'
    }
    ]

    queryUse2 = [{
        'query': 'use',
        'databaseName': 'testdb'
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

    queryInsert2 = [{
        'query': 'insert',
        'tableName': 'orders',
        'attributeN': ['orderNumber', 'orderDate', 'shippedDate', 'status', 'customerNumber'],
        'values': [100, '20-11-2020', '25-11-2020', 'delivered', 1]
    }
    ]

    queryUpdate = [{
        'query': 'update',
        'tableName': 'customers',
        'attributeN': [{'attribute': 'customerName', 'value': 'Diana'}],
        'whereAttribute': 'customerNumber',
        'whereVariable': 3
    }
    ]

    queryDelete = [{
        'query': 'delete',
        'tableName': 'customers',
        'whereAttribute': 'customerName',
        'whereVariable': 'Amelia'
    }
    ]

    queryDelete2 = [{
        'query': 'delete',
        'tableName': 'customers',
        'whereAttribute': 'customerName',
        'whereVariable': 'Amelia2'
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

    queryCreate2 = [{
        'query': 'create',
        'tableName': 'customers',
        'attributeN': 'customerNumber',
        'dataType': 'INT',
        'primaryKey': 'TRUE',
        'foreignKey': 'FALSE',
        'relationshipTable': 'FALSE',
        'relationshipAttribute': 'FALSE'
    },
        {'query': 'create',
         'tableName': 'customers',
         'attributeN': 'customerName',
         'dataType': 'VARCHAR',
         'primaryKey': 'FALSE',
         'foreignKey': 'FALSE',
         'relationshipTable': 'FALSE',
         'relationshipAttribute': 'FALSE'
         },
        {'query': 'create',
         'tableName': 'customers',
         'attributeN': 'customerLastName',
         'dataType': 'VARCHAR',
         'primaryKey': 'FALSE',
         'foreignKey': 'FALSE',
         'relationshipTable': 'FALSE',
         'relationshipAttribute': 'FALSE'
         },
        {'query': 'create',
         'tableName': 'customers',
         'attributeN': 'city',
         'dataType': 'VARCHAR',
         'primaryKey': 'FALSE',
         'foreignKey': 'FALSE',
         'relationshipTable': 'FALSE',
         'relationshipAttribute': 'FALSE'
         },
        {'query': 'create',
         'tableName': 'customers',
         'attributeN': 'postalCode',
         'dataType': 'VARCHAR',
         'primaryKey': 'FALSE',
         'foreignKey': 'FALSE',
         'relationshipTable': 'FALSE',
         'relationshipAttribute': 'FALSE'
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

    # interpretQuery(queryCreateDb2)
    interpretQuery(queryUse2)
    # interpretQuery(querySelect3)
    # interpretQuery(queryCreate)
    # interpretQuery(querySqlDump)
    # interpretQuery(queryErd)
    # interpretQuery(queryCreate2)
    interpretQuery(queryInsert)


# interpretQuery(queryInsert2)
# interpretQuery(queryUpdate)
# interpretQuery(queryDelete2)


def interpretQuery(query):
    global database
    queryType = query[0]['query']

    if queryType == 'create database':
        print("---The query is create database---")
        databaseName = query[0]['databaseName']
        code = executeQueries.createDbQuery(databaseName)
        if code == 0:
            print("The database", databaseName, "already exists")
        elif code == 1:
            print("Database", databaseName, "created")

    elif queryType == 'use':
        print("---The query is use---")
        databaseName = query[0]['databaseName']
        code = executeQueries.useQuery(databaseName)
        if code == 0:
            database = databaseName
            print("Use", database)
        elif code == 1:
            print("Error the database", databaseName, "does not exist")

    elif queryType == 'create':
        print("---The query is create---")
        code = executeQueries.createQuery(database, query)
        if code == 0:
            print("Database not selected")
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
        code = executeQueries.selectQuery(database, query)
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
        code = executeQueries.insertQuery(database, query)
        if code == 0:
            print("Database not selected")
        elif code == 1:
            print("There are values not present in parent table")
        elif code == 2:
            print("Row inserted")
        elif code == 3:
            print("Table does not exist")
        elif code == 4:
            print("An error ocurred")

    elif queryType == 'update':
        print("---The query is update---")
        code = executeQueries.updateQuery(database, query)
        if code == 0:
            print("Database not selected")
        elif code == 1:
            print("Row updated")
        elif code == 2:
            print("Table does not exist")
        elif code == 3:
            print("An error ocurred")

    elif queryType == 'delete':
        print("---The query is delete---")
        code = executeQueries.deleteQuery(database, query)
        if code == 0:
            print("Database not selected")
        elif code == 1:
            print("Row deleted")
        elif code == 2:
            print("Table does not exist")
        elif code == 3:
            print("An error ocurred")

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


if __name__ == "__main__":
    parseQuery()

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
