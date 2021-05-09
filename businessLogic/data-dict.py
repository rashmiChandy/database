import pandas as pd


# -----------------------------------------------------------------------------------------------------
def storein_dataDictionary(tableName, attributeN, dataType, primaryKey, foreignKey, relationshipTable,
                           relationshipAttribute):
    # lowerLimit values
    lowerLimitDict = {"INT": 0,
                      "DECIMAL": 0,
                      "VARCHAR": 0}

    # upperLimit values
    upperLimitDict = {"INT": 2147483647,
                      "DECIMAL": 99999.99999,
                      "VARCHAR": 65535}

    # csv to data frame
    df = pd.read_csv("Data-dictionary.csv")

    if dataType[0] == 'V' or dataType[0] == 'D':
        lowerLimit = lowerLimitDict.get(dataType[0:7])
        upperLimit = upperLimitDict.get(dataType[0:7])
    else:
        lowerLimit = lowerLimitDict.get(dataType)
        upperLimit = upperLimitDict.get(dataType)

    table = df.loc[df['table'] == tableName]

    if not table.empty:
        # print(table)

        attribute = table.loc[df['attribute'] == attributeN]
        if not attribute.empty:
            # print(attribute)
            print("The attribute", attributeN, "already exist in table", tableName)

        else:
            print("The attribute", attributeN, "does NOT exist in table", tableName)
            new_row = {'table': tableName, 'attribute': attributeN, 'dataType': dataType, 'lowerLimit': lowerLimit,
                       'upperLimit': upperLimit,
                       'primaryKey': primaryKey, 'foreignKey': foreignKey, 'relationshipTable': relationshipTable,
                       'relationshipAttribute': relationshipAttribute}
            # append row to the dataframe
            df = df.append(new_row, ignore_index=True)

    else:
        print("The table", tableName, "does not exist in the database")
        new_row = {'table': tableName, 'attribute': attributeN, 'dataType': dataType, 'lowerLimit': lowerLimit,
                   'upperLimit': upperLimit,
                   'primaryKey': primaryKey, 'foreignKey': foreignKey, 'relationshipTable': relationshipTable,
                   'relationshipAttribute': relationshipAttribute}
        df = df.append(new_row, ignore_index=True)

    # saving the dataframe
    df.to_csv('Data-dictionary.csv', index=False)


# -----------------------------------------------------------------------------------------------------
def iterateQueries(queriesData):
    for dic in queriesData:
        print(dic['tableName'], dic['attributeN'], dic['dataType'], dic['primaryKey'], dic['foreignKey'],
              dic['relationshipTable'], dic['relationshipAttribute'])
        storein_dataDictionary(dic['tableName'], dic['attributeN'], dic['dataType'], dic['primaryKey'],
                               dic['foreignKey'], dic['relationshipTable'], dic['relationshipAttribute'])


# -----------------------------------------------------------------------------------------------------
queriesData = [{'tableName': 'orders',
                'attributeN': 'orderNumber',
                'dataType': 'INT',
                'primaryKey': 'TRUE',
                'foreignKey': 'FALSE',
                'relationshipTable': 'FALSE',
                'relationshipAttribute': 'FALSE'
                },
               {'tableName': 'orders',
                'attributeN': 'orderDate',
                'dataType': 'VARCHAR',
                'primaryKey': 'FALSE',
                'foreignKey': 'FALSE',
                'relationshipTable': 'FALSE',
                'relationshipAttribute': 'FALSE'
                },
               {'tableName': 'orders',
                'attributeN': 'shippedDate',
                'dataType': 'VARCHAR',
                'primaryKey': 'FALSE',
                'foreignKey': 'FALSE',
                'relationshipTable': 'FALSE',
                'relationshipAttribute': 'FALSE'
                },
               {'tableName': 'orders',
                'attributeN': 'status',
                'dataType': 'VARCHAR',
                'primaryKey': 'FALSE',
                'foreignKey': 'FALSE',
                'relationshipTable': 'FALSE',
                'relationshipAttribute': 'FALSE'
                },
               {'tableName': 'orders',
                'attributeN': 'customerNumber',
                'dataType': 'INT',
                'primaryKey': 'FALSE',
                'foreignKey': 'TRUE',
                'relationshipTable': 'customers',
                'relationshipAttribute': 'customerNumber'
                }
               ]

iterateQueries(queriesData)
