import logging

from businessLogic import Controller
from main_module.AuthenticationMechanism import AuthenticationMechanism


def get_user_option():
    print("|************** Welcome to Custom My SQL Database **************|")
    print("1. New user")
    print("2. Existing user")
    print("3. MySQL Command prompt")
    print("4. MySQL Dump")
    print("5. Export ERD")
    print("6. Exit from application")


def create_mysqldump_dictionary(path_and_filename):
    return {"query": 'mysqldump',
            "pathAndFilename": path_and_filename
            }


def mysql_command_prompt():
    mysql_query = input('SQL>')
    return mysql_query


def create_erd_dictionary(path_and_filename):
    return {"query": 'export erd',
            "pathAndFilename": path_and_filename
            }


def create_use_dictionary(database_name):
    return {
        "query": 'use',
        "databaseName": database_name
    }


def validate_init(query):
    duplicate_query = query.lower()
    if duplicate_query.find('create database') != -1:
        query_type = 'create database'
    else:
        query_type = query.split(" ")[0]
    return {"query": query_type.lower()}


if __name__ == '__main__':
    logger = logging.getLogger('MySQL_logger')
    logging.basicConfig(filename='5408_G10_.log', filemode='a',
                        format='%(asctime)s - [%(process)d] - %(levelname)s - %(message)s', level=logging.DEBUG)
    logging.info('!!************* DATABASE & DATABASE MANAGEMENT SYSTEM *************!!')
    logging.error('error log example')
    logging.info('info log example')
    logging.debug('debug log example')
    logging.warning('warning log example')
    authentication = AuthenticationMechanism()

    print("|************** Welcome to Custom My SQL Database **************|")
    print("1. New user")
    print("2. Existing user")
    print("3. MySQL Command prompt")
    print("4. MySQL Dump")
    print("5. Export ERD")
    print("6. Exit from application")
    authentication.user_input("Select one of option from above:")
    option = authentication.value
    keep_on = True
    while keep_on and option != 6:
        if option == '1':
            logging.info('*************** Create user module initialization ***************')
            authentication.user_input("Enter SQL username:")
            username = authentication.value
            authentication.user_input("Enter your password:")
            password = authentication.value
            authentication.create_user(username.lower(), password)
            logging.info('*************** Create user module end ***************')

            get_user_option()
            authentication.user_input("Select one of option from above:")
            option = authentication.value
        elif option == '2':
            logging.info('*************** Verify user initialization ***************')
            authentication.user_input("Enter SQL username:")
            username = authentication.value
            authentication.user_input("Enter your password:")
            password = authentication.value
            authentication.verify_user(username.lower(), password)
            logging.info('*************** Verify user end ***************')
            get_user_option()
            authentication.user_input("Select one of option from above:")
            option = authentication.value
        elif option == '3':
            print('\n*************** Welcome to My SQL Command Prompt *************** ')
            print('Command to exit command:logout')
            logging.info('*************** My SQL command prompt ***************')
            user_provided_query = mysql_command_prompt()
            while user_provided_query != 'logout':
                interpret_query = validate_init(user_provided_query)
                Controller.interpretQuery([interpret_query], user_provided_query)
                if user_provided_query != 'logout':
                    user_provided_query = mysql_command_prompt()

            get_user_option()
            authentication.user_input("Select one of option from above:")
            option = authentication.value
        elif option == '4':
            logging.info('*************** My SQL dump ***************')
            print('\n*************** My SQL dump *************** ')
            username_for_dump = input('Enter the username:')
            database_for_dump = input('Enter the database name:')
            filepath_for_dump = input('Enter the filepath for dump:')
            Controller.interpretQuery([create_use_dictionary(database_for_dump)], 'USE ' + database_for_dump)
            print('mysqldump -u ' + username_for_dump + ' -p ' + database_for_dump + ' > ' + filepath_for_dump)
            user_provided_query = 'mysqldump -u ' + username_for_dump + ' -p ' + database_for_dump + ' > ' + filepath_for_dump;
            mysql_dump_query = create_mysqldump_dictionary(filepath_for_dump)
            Controller.interpretQuery([mysql_dump_query], user_provided_query)
            logging.info('*************** My SQL dump ended ***************')
            get_user_option()
            authentication.user_input("Select one of option from above:")
            option = authentication.value

        elif option == '5':
            print('\n*************** Export ERD ***************')
            logging.info('*************** Export ERD ***************')
            filepath_for_erd = input('Enter the filepath for ERD:')
            database_name = input('Enter the database name to export:')
            Controller.interpretQuery([create_use_dictionary(database_name)], 'USE ' + database_name)
            export_query = create_erd_dictionary(filepath_for_erd)
            user_provided_query = 'export erd'
            Controller.interpretQuery([export_query], user_provided_query)
            get_user_option()
            authentication.user_input("Select one of option from above:")
            option = authentication.value

        elif option == '6':
            print('\nDisconnected!')
            keep_on = False
        else:
            print("Invalid option, process aborted!")
            logger.error("Invalid option selected, option:" + option)
            keep_on = False

    logging.info('!!************* DATABASE & DATABASE MANAGEMENT SYSTEM *************!!')
    print("|************** Thank you **************|")
