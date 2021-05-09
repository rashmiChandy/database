import os

import pandas as pd
from businessLogic.methods import dataDictionary, createTableQuery, insertEntryQuery, updateEntryQuery, \
    deleteEntryQuery, erd, \
    sqlDumps

global filepath, filepath_slash
filepath = "C:\\Users\\kethan\\Documents\\databases"
filepath_slash = "\\"


def createDbQuery(database):
    # path = './databases'
    path = filepath
    # path = '.\databases' # windows?
    directory_contents = os.listdir(path)
    if database in directory_contents:
        return 0
    else:
        path += filepath_slash + database
        os.makedirs(path)
        dataDictionary.createDataDictionary(database, path)
        dataDictionary.create_concurrency_status_file(database, path)
        return 1


def useQuery(database):
    path = filepath
    directory_contents = os.listdir(path)
    if database in directory_contents:
        return 0
    return 1


def createQuery(database, query):
    # path = './databases'
    path = filepath
    if database == "":
        return 0
    else:
        directory_contents = os.listdir(path)
        if database in directory_contents:
            path += filepath_slash + database
            directory_contents = os.listdir(path)
            tableName = query[0]['tableName'] + ".csv"
            if tableName in directory_contents:
                return 1
            else:
                result = createTableQuery.checkForeignTables(query, path, database)
                if not result:
                    return 2
                createTableQuery.createTableFile(query, path, database, tableName)
                dataDictionary.addTableDataDictionary(query, path, database)  # save table in data dictionary
                dataDictionary.add_table_to_concurrency_status(query, path, database)  # save table name for concurrency
                return 3
        else:
            return 4


def selectQuery(database, query):
    path = filepath
    if database == "":
        return 0
    else:
        directory_contents = os.listdir(path)
        result = []
        if database in directory_contents:
            path += filepath_slash + database
            directory_contents = os.listdir(path)
            tableName = query[0]['tableName'] + ".csv"
            csvFileName = path + filepath_slash + tableName
            if tableName in directory_contents:
                df = pd.read_csv(csvFileName)
                whereAttribute = query[0]['whereAttribute']
                whereVariable = query[0]['whereVariable']
                attributeN = query[0]['attributeN'][0]

                if whereAttribute == "FALSE" and attributeN == "*":
                    result = df
                elif whereAttribute != "FALSE" and attributeN == "*":
                    result = df.loc[df[whereAttribute] == whereVariable]
                elif whereAttribute != "FALSE" and attributeN != "*":
                    listAttributes = query[0]['attributeN']
                    df = df[listAttributes]
                    result = df.loc[df[whereAttribute] == whereVariable]
                return [1, result]
            else:
                return 2
        else:
            return 3


def insertQuery(database, query):
    path = filepath
    if database == "":
        return 0
    else:
        directory_contents = os.listdir(path)
        if database in directory_contents:
            path += filepath_slash + database
            directory_contents = os.listdir(path)
            tableName = query[0]['tableName'] + ".csv"
            csvFileName = path + filepath_slash + tableName
            if tableName in directory_contents:
                result = insertEntryQuery.verifyValuesinForeignTables(query, path, database, tableName)
                if result == False:
                    return 1
                else:
                    insertEntryQuery.insertValuesinTable(query, path, database, tableName)
                    return 2
            else:
                return 3
        else:
            return 4


def updateQuery(database, query):
    path = filepath
    if database == "":
        return 0
    else:
        directory_contents = os.listdir(path)
        if database in directory_contents:
            path += filepath_slash + database
            directory_contents = os.listdir(path)
            tableName = query[0]['tableName'] + ".csv"
            csvFileName = path + filepath_slash + tableName
            if tableName in directory_contents:
                updateEntryQuery.updateValuesinTable(query, path, database, tableName)
                return 1
            else:
                return 2
        else:
            return 3


def deleteQuery(database, query):
    path = filepath
    if database == "":
        return 0
    else:
        directory_contents = os.listdir(path)
        if database in directory_contents:
            path += filepath_slash + database
            directory_contents = os.listdir(path)
            tableName = query[0]['tableName'] + ".csv"
            csvFileName = path + filepath_slash + tableName
            if tableName in directory_contents:
                deleteEntryQuery.deleteValuesinTable(query, path, database, tableName)
                return 1
            else:
                return 2
        else:
            return 3


def mysqldumpQuery(database, query):
    # path = './databases'
    path = filepath
    if database == "":
        return 0
    else:
        dataDictName = "dataDict-" + database + ".csv"
        path += filepath_slash + database
        directory_contents = os.listdir(path)
        if dataDictName in directory_contents:
            sqlDumps.generatesqlDump(query, path, dataDictName)
            return 1
        else:
            return 2


def exporterdQuery(database, query):
    # path = './databases'
    path = filepath
    if database == "":
        return 0
    else:
        dataDictName = "dataDict-" + database + ".csv"
        path += filepath_slash + database
        directory_contents = os.listdir(path)
        if dataDictName in directory_contents:
            erd.generateErd(query, path, database)
            return 1
        else:
            return 2
