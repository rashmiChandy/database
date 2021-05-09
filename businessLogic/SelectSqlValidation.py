import logging
import re


class SelectSqlValidation:

    def validate_parse_select(self, query):
        logging.debug("Validating Select query.....")
        select_query = []
        query = self.remove_semicolon(self, query)

        if query.find("*") > 0:
            queryMatch = re.search("^select\s[*]\sfrom\s[a-zA-Z0-9\_]+$", query, re.IGNORECASE)
            logging.debug("here")
            logging.debug(queryMatch)

        else:

            queryMatch = re.search("^select\s*([a-zA-Z0-9]+\,?\s?)+from\s*[\w]+(\s*where.+['][\w]+['])?$", query,
                                   re.IGNORECASE)
            logging.debug(queryMatch)

        if queryMatch == None:
            print("Select query Invalid")

        else:
            select_query.append(self.parse_query(self, query))
        return select_query

    def parse_query(self, query):
        from_clause = re.search("from\s[\w]+", query)
        table_name = from_clause.group().split(" ")[1]

        select_clause = query.index("from")
        attribute_names = ['*']
        if query.find("*") == -1:
            attribute_names = query[7:select_clause - 1].split(',')

        where_attribute = 'FALSE'
        where_variable = 'FALSE'

        if query.lower().find("where") > 0:
            where_clause_index = query.lower().index("where")
            equation = query[where_clause_index + 5:].split('=')
            logging.debug(equation)
            where_attribute = equation[0].strip()
            where_variable = equation[1].strip()
            where_variable = re.sub('\'', "", where_variable)
            where_variable = where_variable.replace('\'', '')
            logging.debug(where_attribute)
            logging.debug(where_variable)

        return self.select_dictionary(self, table_name, attribute_names, where_attribute, where_variable)

    def select_dictionary(self, table_name, attribute_name, where_attribute, where_variable):
        return {
            'query': 'select',
            'tableName': table_name,
            'attributeN': attribute_name,
            'whereAttribute': where_attribute,
            'whereVariable': where_variable
        }

    def remove_semicolon(self, query):
        if query.find(";") > -1:
            query = query.replace(';', '')
        return query
