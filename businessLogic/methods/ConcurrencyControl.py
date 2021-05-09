import logging
import time

import pandas as pd

filepath = "C:\\Users\\kethan\\Documents\\databases"
filepath_slash = "\\"
status = "\\status-"
dataDict = "\\dataDict-"


def concurrency_control(database, table_name, flip):
    table_name = table_name[:-4]
    time_end = time.time() + 60 * 0.1  # wait for status to change
    if flip:
        value = 'no'
        while time.time() < time_end:
            status_file_path = filepath + filepath_slash + database + status + database + ".csv"  # open status file
            df = pd.read_csv(status_file_path)
            df_table = df.loc[df['table'] == table_name]
            logging.debug(df_table['table'])
            logging.debug(df_table['inUse'])
            if df_table['table'].any() == table_name:
                if df_table['inUse'].any() == value:
                    if (df_table['inUse'] == value).any():
                        index_list = df_table.index[df_table['table'] == table_name].tolist()
                        for i in index_list:
                            logging.debug('Locking table for concurrency control:' + table_name)
                            df.at[i, 'inUse'] = 'yes'
                        df.to_csv(status_file_path, index=False)
                        return True
            logging.debug('Concurrency control | Waiting for table to unlock')
        print('Concurrency control | Could not get the lock for table:' + table_name)
        print('Concurrency control | Please try again!')
        return False
    else:
        value = 'yes'
        while time.time() < time_end:
            status_file_path = filepath + filepath_slash + database + status + database + ".csv"  # open status file
            df = pd.read_csv(status_file_path)
            df_table = df.loc[df['table'] == table_name]
            if df_table['table'].any() == table_name:
                if df_table['inUse'].any() == value:
                    if (df_table['inUse'] == value).any():
                        index_list = df_table.index[df_table['table'] == table_name].tolist()
                        for i in index_list:
                            logging.debug('Unlocking table for concurrency control:' + table_name)
                            df.at[i, 'inUse'] = 'no'
                        df.to_csv(status_file_path, index=False)
                        return True
        return False
