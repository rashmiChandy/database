import logging
import re
from decimal import Decimal


class UpdateSqlValidation:

    def validate_parse_update(self, query):
        logging.debug("Validating Update Query...")
        query = self.remove_semicolon(self, query)

        queryMatch = re.search("^update\s[\w]+\sSET\s.*\swhere\s[\w]+\s=\s[']?[\w]+[']?$", query, re.IGNORECASE)
        if queryMatch:
            table_name = query.split(" ")[1]

            where_attribute = 'FALSE'
            where_variable = 'FALSE'
            if query.lower().find("where") > 0:
                where_clause = query.lower().index("where")
                equation = query[where_clause + 5:].split('=')
                logging.debug(equation)
                where_attribute = equation[0].strip()
                where_variable = equation[1].strip()
                where_variable = where_variable.replace('\'', '')
                if where_variable.isnumeric():
                    where_variable = int(where_variable)
                elif where_variable.isdecimal():
                    where_variable = Decimal(where_variable)

            set_update_query = re.search("[\w]+\s*=\s*['].+[']", query, re.IGNORECASE)
            set_attribute_list = set_update_query.group().split('=')
            attribute = set_attribute_list[0].strip()
            value = set_attribute_list[1].strip()

            return [
                self.select_dictionary(self, table_name, [{"attribute": attribute, "value": value}], where_attribute,
                                       where_variable)]
        else:
            print("Update query Invalid")

    def select_dictionary(self, table_name, attribute_name, where_attribute, where_variable):
        return {
            'query': 'update',
            'tableName': table_name,
            'attributeN': attribute_name,
            'whereAttribute': where_attribute,
            'whereVariable': where_variable
        }

    def remove_semicolon(self, query):
        if query.find(";") > -1:
            query = query.replace(';', '')
        return query
