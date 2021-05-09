import datetime
import logging
import os

import pandas as pd
import pyAesCrypt


class AuthenticationMechanism:

    def __init__(self):
        self.value = ""
        self.user_exists = False
        self.verify_user_call = False
        self.password = "!**)^^__87*"

    def user_input(self, message):
        self.value = input(message)
        if len(self.value) == 0:
            self.user_input(message)

    def user_store(self, new_username, new_user_password):
        current_time = datetime.datetime.now()
        logging.info('|== Authentication mechanism initialization ==|')
        buffer_size = 64 * 1024
        encrypted_filename = "users_store.enc"
        decrypted_filename = "temporary.csv"

        try:
            pyAesCrypt.decryptFile(encrypted_filename, decrypted_filename, self.password, buffer_size)
            logging.debug('Successfully decrypted user_store.enc')
        except FileNotFoundError as ie:
            logging.error('File does not exist')
            logging.exception(ie)
            logging.error('Could not decrypt user_store.enc')
        except Exception as e:
            logging.error('Exception occurred')
            logging.exception(e)
            logging.error('Could not decrypt user_store.enc')

        existing_data_frame = pd.read_csv(decrypted_filename)
        username_count = existing_data_frame[existing_data_frame['username'].str.contains(new_username)]

        if len(username_count) > 0:
            if self.verify_user_call:
                logging.info('User exists in the encrypted user store')

                for i in range(len(existing_data_frame)):
                    if new_username == existing_data_frame.loc[i, "username"]:
                        if new_user_password == existing_data_frame.loc[i, "password"]:
                            self.user_exists = True
                            print('User authentication successful, login time:' + current_time.__str__())
                            logging.info(
                                'User authentication successful for user:' + new_username + ', Login time:' + current_time.__str__())
                if os.path.exists(decrypted_filename):
                    os.remove(decrypted_filename)
                    logging.info('Temporary')
                else:
                    logging.info('The decrypt file does not exist')
                return
            print('User already exists, choose a different name!')
            logging.info('User already exists, choose a different name!')
        elif not self.verify_user_call:
            user_data = open(decrypted_filename, "a")
            user_details = ["\n" + new_username + "," + new_user_password]
            user_data.writelines(user_details)
            user_data.close()
            print("User Created Successfully, creation time:" + current_time.__str__())
            try:
                pyAesCrypt.encryptFile(decrypted_filename, encrypted_filename, self.password, buffer_size)
            except Exception as e:
                logging.error('Exception occurred')
                logging.exception(e)

        if os.path.exists(decrypted_filename):
            os.remove(decrypted_filename)
        else:
            print("The file does not exist")

        logging.info('|== Authentication mechanism end ==|')

    def create_user(self, username, password):
        self.user_store(username, password)

    def verify_user(self, username, password):
        self.verify_user_call = True
        self.user_store(username, password)
        self.verify_user_call = False
        if not self.user_exists:
            print('Invalid username or password, authentication unsuccessful')
            logging.info('Invalid username or password, provided username:' + username)
        return self.user_exists
