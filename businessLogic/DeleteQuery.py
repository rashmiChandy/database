import logging
import re
from decimal import Decimal


def create_delete_dictionary(table_name, where_attribute, where_variable):
    return {"query": 'delete',
            "tableName": table_name,
            "whereAttribute": where_attribute,
            "whereVariable": where_variable
            }


def get_data_inside_brackets(word):
    start = word.index("(") + 1
    end = word.index(")", start)
    return word[start:end]


def delete_query(query):
    logging.debug('Delete query initialization')
    if query:
        try:
            statement = re.search(r"DELETE FROM ([\w]+)\s+WHERE\s[\w]+\s=\s[']?[\w]+[']?", query, re.IGNORECASE)
            if statement:
                values_part = query.split("FROM")
                if values_part:
                    delete_table_name = values_part[1].split("WHERE")[0].strip()
                    logging.debug('table name:' + delete_table_name)
                    attributes = values_part[1].split("WHERE")
                    where_attribute = attributes[1].split("=")[0].strip()
                    where_variable = attributes[1].split("=")[1].strip().split(";")[0]
                    where_variable = re.sub('\'', "", where_variable)
                    where_variable = where_variable.replace('\'', '')
                    if where_variable.isnumeric():
                        where_variable = int(where_variable)
                    elif where_variable.isdecimal():
                        where_variable = Decimal(where_variable)

                    dictionary = create_delete_dictionary(delete_table_name, where_attribute, where_variable)

                    logging.debug(dictionary)
                    logging.debug('Delete dictionary:')
                    logging.debug(dictionary)
                    return [dictionary]
        except Exception as ex:
            logging.exception(ex)
            print('Invalid DELETE query, please check!')
