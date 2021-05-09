import pandas as pd


def generatesqlDump():
    # csv to data frame
    df = pd.read_csv("Data-dictionary.csv")
    df = df[
        ['table', 'attribute', 'dataType', 'primaryKey', 'foreignKey', 'relationshipTable', 'relationshipAttribute']]
    # print(df)

    table_names = df.table.unique()
    # print(table_names)
    df_sqlDump = pd.DataFrame(
        columns=['table', 'attribute', 'dataType', 'primaryKey', 'foreignKey', 'relationshipTable',
                 'relationshipAttribute'])
    # print(df_sqlDump)

    for t in table_names:
        # print(t)
        df_sqlDump = df_sqlDump.append(df.loc[df['table'] == t], ignore_index=True)
        # print(df_sqlDump)
        new_row = {'table': "", 'attribute': "", 'dataType': "",
                   'primaryKey': "", 'foreignKey': "", 'relationshipTable': "", 'relationshipAttribute': ""}
        df_sqlDump = df_sqlDump.append(new_row, ignore_index=True)

    # print(df_sqlDump)
    # saving the dataframe
    df_sqlDump.to_csv('sql-dump.csv', index=False)
    print("sql-dump.csv saved")


# -----------------------------------------------------------------------------------------------------

generatesqlDump()
