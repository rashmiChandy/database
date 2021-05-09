import logging
import re


class CreateValidation:

    def __init__(self):
        print("Validation and Parsing of sql query")

    def validate_parse_use_db(self, query):
        query = self.remove_semicolon(self, query)
        use_dictionary = []
        queryString = re.search("^(USE)\s[\w]+$", query, re.IGNORECASE)
        if queryString:
            use_query = queryString.string.split(" ")
            use_dictionary = {'query': use_query[0].strip(), 'databaseName': use_query[1].strip()}
        else:
            print("Use Database query Invalid")
        return [use_dictionary]

    def validate_parse_create_db(self, query):
        query = self.remove_semicolon(self, query)
        queryData = []
        queryString = re.search("(CREATE)\s(DATABASE)\s[\w]+", query, re.IGNORECASE)
        logging.debug(queryString)
        if queryString == None:
            print("Create Database query Invalid")
        else:
            database_name = queryString.string.split(" ")[2]
            queryData.append(self.create_db_dictionary(self, database_name))

        return queryData

    def validate_parse_create_query(self, query):
        queryData = []
        query = self.remove_semicolon(self, query)
        queryString = re.search("(CREATE)\sTABLE\s[\w]+\s*\(.+\)", query, re.IGNORECASE)
        logging.debug(queryString)
        if queryString:
            split_query = queryString.string.split(" ")
            table_name = split_query[2]
            logging.debug(table_name)

            indexOfBracket = query.find('(')
            lastIndexOfBracket = query.rindex(")")

            columnString = query[indexOfBracket + 1:lastIndexOfBracket]
            columns = columnString.split(',')
            logging.debug(columns)
            for column in columns:
                logging.debug(column)
                matchedColumn = re.search("[\w]+\s[\w]+(\([0-9]+\))?", column)
                if matchedColumn is not None and not (
                        matchedColumn.string.lower().startswith("primary") or matchedColumn.string.lower().startswith(
                        "foreign")):
                    logging.debug(matchedColumn)
                    columnData = column.split(" ")
                    queryData.append(
                        self.create_dictionary(self, table_name, columnData[0], columnData[1], 'FALSE', 'FALSE',
                                               'FALSE', 'FALSE'))

                matchedPrimary = re.search("(PRIMARY KEY){1}\s*\([a-zA-Z]+\){1}", column, re.IGNORECASE)

                if matchedPrimary is not None:
                    logging.debug(matchedPrimary)
                    primaryColumnName = self.get_data_inside_brackets(self, matchedPrimary.string)
                    self.update_dictionary(self, primaryColumnName, "primaryKey", "TRUE", queryData)
                    logging.debug(primaryColumnName)

                matchedForeign = re.search(
                    "(FOREIGN KEY){1}\s*(\([a-zA-Z]+\)){1}\s+(REFERENCES\s+[\w]+(\s)*(\([a-zA-Z]+\))){1}", column,
                    re.IGNORECASE)
                if matchedForeign is not None:
                    self.check_foreign_key(self, matchedForeign, column, queryData)

        else:
            print("Create Query Invalid")
        return queryData

    def check_foreign_key(self, matchedForeign, column, queryData):
        foreign_column_name = self.get_data_inside_brackets(self, matchedForeign.string)
        self.update_dictionary(self, foreign_column_name, "foreignKey", "TRUE", queryData)
        logging.debug(matchedForeign)
        matched_referenced_table = re.search("(REFERENCES){1}\s+[\w]+(\s)*(\([a-zA-Z]+\)){1}", column, re.IGNORECASE)
        if matched_referenced_table is not None:
            referenced_table_name = column.split(" ")[4]
            referenced_table_name = referenced_table_name.split('(')[0]
            referenced_column_name = self.get_data_inside_brackets(self, matched_referenced_table.string)
            self.update_dictionary(self, foreign_column_name, "foreignKey", "TRUE", queryData)
            self.update_dictionary(self, foreign_column_name, "relationshipTable", referenced_table_name, queryData)
            self.update_dictionary(self, foreign_column_name, "relationshipAttribute", referenced_column_name,
                                   queryData)
            return True
        else:
            return False

    def create_dictionary(self, table_name, attribute_name, data_type, primary_key, foreign_key, relationship_table,
                          relationship_attribute):
        return {'query': 'create',
                "tableName": table_name,
                "attributeN": attribute_name,
                "dataType": data_type,
                "primaryKey": primary_key,
                "foreignKey": foreign_key,
                "relationshipTable": relationship_table,
                "relationshipAttribute": relationship_attribute
                }

    def create_db_dictionary(self, database_name):
        return {'query': 'create database',
                "databaseName": database_name
                }

    def update_dictionary(self, attribute_name, key, value, query_data):
        for column_dictionary in query_data:
            if column_dictionary["attributeN"] == attribute_name:
                column_dictionary[key] = value

    def get_data_inside_brackets(self, word):
        start = word.index("(") + 1
        end = word.index(")", start)
        return word[start:end]

    def remove_semicolon(self, query):
        if query.find(";") > -1:
            query = query.replace(';', '')
        return query
