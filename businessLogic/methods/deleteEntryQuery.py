import logging

import pandas as pd
from businessLogic.methods import ConcurrencyControl

filepath = "C:\\Users\\kethan\\Documents\\databases"
filepath_slash = "\\"


def deleteValuesinTable(query, path, database, tableName):
    con_status = False
    try:
        con_status = ConcurrencyControl.concurrency_control(database, tableName, True)
        if con_status == True:
            pathTable = path + filepath_slash + tableName
            df = pd.read_csv(pathTable)
            logging.debug(df)
            whereAttribute = query[0]['whereAttribute']
            whereValue = query[0]['whereVariable']

            logging.debug(whereAttribute)
            logging.debug(whereValue)

            df.drop(df[df[whereAttribute] == whereValue].index, inplace=True)

            logging.debug(df)
            df.to_csv(pathTable, index=False)
    finally:
        if con_status == True:
            ConcurrencyControl.concurrency_control(database, tableName, False)

    return 0
