import pandas as pd

from businessLogic.methods import ConcurrencyControl

global filepath, filepath_slash
filepath = "C:\\Users\\kethan\\Documents\\databases"
filepath_slash = "\\"


def updateValuesinTable(query, path, database, tableName):
    con_status = False
    try:
        con_status = ConcurrencyControl.concurrency_control(database, tableName, True)
        if con_status == True:
            pathTable = path + filepath_slash + tableName
            df = pd.read_csv(pathTable)
            attributeToUpdate = query[0]['attributeN'][0]['attribute']
            valueToInsert = query[0]['attributeN'][0]['value']
            whereAttribute = query[0]['whereAttribute']
            whereValue = query[0]['whereVariable']
            indexList = df.index[df[whereAttribute] == whereValue].tolist()

            for i in indexList:
                df.at[i, attributeToUpdate] = valueToInsert

            df.to_csv(pathTable, index=False)
    finally:
        if con_status == True:
            ConcurrencyControl.concurrency_control(database, tableName, False)
    return 0
