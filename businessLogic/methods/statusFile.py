import pandas as pd


def createStatusFile(database, path):
    df_status = pd.DataFrame(columns=['table', 'inUse'])
    pathStatusFile = path + "/status-" + database + ".csv"
    df_status.to_csv(pathStatusFile, index=False)
    return 0


def addTableStatusFile(query, path, database):
    pathStatusFile = path + "/status-" + database + ".csv"
    df = pd.read_csv(pathStatusFile)
    tableName = query[0]['tableName']
    new_row = {'table': tableName, 'inUse': 'no'}
    df = df.append(new_row, ignore_index=True)
    df.to_csv(pathStatusFile, index=False)
