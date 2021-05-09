import logging
import re
from decimal import Decimal


def create_insert_dictionary(table_name, attribute_name, values):
    return {"query": 'insert',
            "tableName": table_name,
            "attributeN": attribute_name,
            "values": values,
            }


def get_data_inside_brackets(word):
    start = word.index("(") + 1
    end = word.index(")", start)
    return word[start:end]


def insert_query(query):
    logging.debug('Insert query initialization')
    flag = False
    if query:
        try:
            statement = re.search(r"INSERT INTO ([\w]+)\s*\(.+\) VALUES\s*\(.+\);", query, re.IGNORECASE)
            values_part = query.split("VALUES")
            logging.info('Insert query validation')
            insert_table_name = query.split("(")[0].split("INTO")[1].strip()
            logging.debug('Table name:')
            logging.debug(insert_table_name)
            insert_part = get_data_inside_brackets(statement.string)
            values_part1 = get_data_inside_brackets(values_part[1])
            logging.debug('Insert part:' + insert_part)
            logging.debug('Values part:' + values_part1)
            values_part1 = re.sub('\'', "", values_part1)

            list_of_values = values_part1.split(",")
            for i in range(0, len(list_of_values)):
                list_of_values[i] = list_of_values[i].strip()
                values_part1_regex = re.search(r"([\w]+[.]?)", list_of_values[i])
                if list_of_values[i].isnumeric():
                    list_of_values[i] = int(list_of_values[i])
                elif list_of_values[i].isdecimal():
                    list_of_values[i] = Decimal(list_of_values[i])

            insert_part_regex = re.search(r"([a-zA-Z0-9]+\,?)+$", insert_part)

            if insert_part_regex:
                flag = True
                logging.debug(insert_part_regex.string)
            if values_part1_regex:
                flag = True
                logging.debug(values_part1_regex.string)
            if flag:
                dictionary = create_insert_dictionary(insert_table_name, insert_part.split(","), list_of_values)
                logging.debug(dictionary)
                logging.debug('Insert dictionary:')
                logging.debug(dictionary)
                return [dictionary]
        except Exception as ex:
            logging.exception(ex)
            print('Invalid INSERT query, please check!')
