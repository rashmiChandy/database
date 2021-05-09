import logging

import pandas as pd

status = "\\status-"
dataDict = "\\dataDict-"


def createDataDictionary(database, path):
    df_dataDict = pd.DataFrame(
        columns=['table', 'attribute', 'dataType', 'lowerLimit', 'upperLimit', 'primaryKey', 'foreignKey',
                 'relationshipTable', 'relationshipAttribute'])
    csv_file_name = path + dataDict + database + ".csv"
    logging.debug('Created data dictionary for database:' + database)
    df_dataDict.to_csv(csv_file_name, index=False)
    return 0


def create_concurrency_status_file(database, path):
    df_status_dict = pd.DataFrame(
        columns=['table', 'inUse'])
    csv_file_name = path + status + database + ".csv"
    logging.debug('Created concurrency status file for database:' + database)
    df_status_dict.to_csv(csv_file_name, index=False)
    return 0


def storeinDataDictionary(df, tableName, attributeN, dataType, primaryKey, foreignKey, relationshipTable,
                          relationshipAttribute):
    # lowerLimit values
    lowerLimitDict = {"INT": 0,
                      "DECIMAL": 0,
                      "VARCHAR": 0}
    # upperLimit values
    upperLimitDict = {"INT": 2147483647,
                      "DECIMAL": 99999.99999,
                      "VARCHAR": 65535}
    if dataType[0] == 'V' or dataType[0] == 'D':
        lowerLimit = lowerLimitDict.get(dataType[0:7])
        upperLimit = upperLimitDict.get(dataType[0:7])
    else:
        lowerLimit = lowerLimitDict.get(dataType)
        upperLimit = upperLimitDict.get(dataType)

    new_row = {'table': tableName, 'attribute': attributeN, 'dataType': dataType, 'lowerLimit': lowerLimit,
               'upperLimit': upperLimit,
               'primaryKey': primaryKey, 'foreignKey': foreignKey, 'relationshipTable': relationshipTable,
               'relationshipAttribute': relationshipAttribute}
    df = df.append(new_row, ignore_index=True)
    return df


def addTableDataDictionary(query, path, database):
    path += dataDict + database + ".csv"
    df = pd.read_csv(path)
    for dic in query:
        df = storeinDataDictionary(df, dic['tableName'], dic['attributeN'], dic['dataType'], dic['primaryKey'],
                                   dic['foreignKey'], dic['relationshipTable'], dic['relationshipAttribute'])
    df.to_csv(path, index=False)


def add_table_to_concurrency_status(query, path, database):
    path += status + database + ".csv"
    df = pd.read_csv(path)
    table_name = ''
    for concur_dict in query:
        table_name = concur_dict['tableName']
    new_row = {'table': table_name, 'inUse': 'no'}
    if table_name != '':
        logging.debug('Updated concurrency status file with table name:' + table_name)
        df = df.append(new_row, ignore_index=True)
        df.to_csv(path, index=False)
    return df
