import warnings

import pandas as pd
from businessLogic.methods import ConcurrencyControl

filepath = "C:\\Users\\kethan\\Documents\\databases"
filepath_slash = "\\"
status = "\\status-"
dataDict = "\\dataDict-"


def verifyValuesinForeignTables(query, path, database, tableName):
    # open data dictionary and get the relationships of the attributes of that table! in this case orders
    pathDataDict = path + dataDict + database + ".csv"
    df = pd.read_csv(pathDataDict)
    df = df.loc[df['table'] == query[0]['tableName']]

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',
                                r'elementwise comparison failed; returning scalar instead, but in the future will '
                                r'perform elementwise comparison(.*)')
        df_foreignK = df.loc[(df['relationshipTable'] != 'FALSE') & (df['relationshipTable'] != 'False') & (
                df['relationshipTable'] != False)]

    # print(df_foreignK)
    foreignAttributes = []
    for index, row in df_foreignK.iterrows():  # iterating over the dictionary elements of the table we want to insert
        dic = {}
        dic['attribute'] = row['attribute']
        dic['relationshipTable'] = row['relationshipTable']
        dic['relationshipAttribute'] = row['relationshipAttribute']
        foreignAttributes.append(dic)

    # print(foreignAttributes)
    for dic in foreignAttributes:
        # open the table where they belong
        currentTableAttribute = dic['attribute']
        foreignTable = dic['relationshipTable']
        foreignAttribute = dic['relationshipAttribute']
        value = ''
        pathTable = path + filepath_slash + foreignTable + ".csv"  # open foreign table
        df_foreignTable = pd.read_csv(pathTable)
        attributesToInsert = query[0]['attributeN']
        valuesToInsert = query[0]['values']

        if foreignAttribute in attributesToInsert:  # check if foreignAttribute is in the list of attributes to insert
            index = attributesToInsert.index(dic['relationshipAttribute'])
            value = valuesToInsert[index]
        # print(df_foreignTable)
        if (df_foreignTable[foreignAttribute] == value).any():  # check if table and attribute exist in data dictionary
            # print("The attribute",foreignAttribute, "with value", value, "is in parent table", foreignTable)
            return True
        else:
            # print("The attribute",foreignAttribute, "with value", value, "is NOT in parent table", foreignTable)
            return False


def insertValuesinTable(query, path, database, tableName):
    # result =  checkStatusFile(path, database,  tableName)
    # print(result) # here if its true we can perform the insert if not we cannot
    con_status = False
    try:
        con_status = ConcurrencyControl.concurrency_control(database, tableName, True)
        if con_status == True:
            pathTable = path + filepath_slash + tableName
            df = pd.read_csv(pathTable)
            attributesToInsert = query[0]['attributeN']
            valuesToInsert = query[0]['values']
            lenghtAttributesToInsert = len(attributesToInsert)
            new_row = {}
            for i in range(lenghtAttributesToInsert):
                new_row[attributesToInsert[i]] = valuesToInsert[i]

            df = df.append(new_row, ignore_index=True)
            df.to_csv(pathTable, index=False)
    except:
        print('Exception in insertEntryQuery')
    finally:
        if con_status == True:
            ConcurrencyControl.concurrency_control(database, tableName, False)

    return 0
