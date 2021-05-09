import pandas as pd


def generatesqlDump(query, path, dataDictName):
    dataDictPath = path + "/" + dataDictName
    df = pd.read_csv(dataDictPath)
    columnsDump = ['table', 'attribute', 'dataType', 'primaryKey', 'foreignKey', 'relationshipTable',
                   'relationshipAttribute']
    df = df[columnsDump]
    table_names = df.table.unique()
    df_sqlDump = pd.DataFrame(columns=columnsDump)  # create new data frame

    for t in table_names:
        df_sqlDump = df_sqlDump.append(df.loc[df['table'] == t], ignore_index=True)  # extract a part of the data dict
        new_row = {'table': "", 'attribute': "", 'dataType': "", 'primaryKey': "", 'foreignKey': "",
                   'relationshipTable': "", 'relationshipAttribute': ""}  # save empty row
        df_sqlDump = df_sqlDump.append(new_row, ignore_index=True)

    sqlDumpfileName = query[0]['pathAndFilename'] + ".csv"
    df_sqlDump.to_csv(sqlDumpfileName, index=False)  # saving the dataframe
