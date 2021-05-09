import pandas as pd


def generateErd(query, path, database):
    path += "/dataDict-" + database + ".csv"
    df = pd.read_csv(path)
    columnsDump = ['table', 'attribute', 'relationshipTable', 'relationshipAttribute']
    df_columnsDump = df[columnsDump]
    # columns = ['table','attribute', 'dataType']
    # df_colums = df[columns]
    df_erd = df_columnsDump.loc[
        (df_columnsDump['relationshipTable'] != 'FALSE') & (df_columnsDump['relationshipTable'] != 'False')]
    textFilename = query[0]['pathAndFilename'] + ".txt"
    f = open(textFilename, "w")
    f.write("Table1 -> Table2 | KeyTable1 - KeyTable2 \n\n")
    for index, row in df_erd.iterrows():
        f.write(row['table'] + " -> " + row['relationshipTable'] + " | " + row['attribute'] + " - " + row[
            'relationshipAttribute'] + "\n")

    f.close()
