import pandas as pd


def checkForeignTables(query, path, database):
    path += "\\dataDict-" + database + ".csv"
    df = pd.read_csv(path)
    for dic in query:
        relationshipTable = dic['relationshipTable']
        relationshipAttribute = dic['relationshipAttribute']
        if relationshipTable != 'FALSE':
            if ((df['table'] == relationshipTable) & (df[
                                                          'attribute'] == relationshipAttribute)).any():  # check if
                # table and attribute exist in data dictionary
                dummy = 1
            else:
                return False
    return True


def createTableFile(query, path, database, tableName):
    tableAttributes = []
    for dic in query:
        tableAttributes.append(dic['attributeN'])

    df_table = pd.DataFrame(columns=tableAttributes)  # save table file
    csvFileName = path + "\\" + tableName
    df_table.to_csv(csvFileName, index=False)
