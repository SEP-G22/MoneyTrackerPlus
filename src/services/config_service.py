# This file contains the ConfigService class which is responsible for reading and writing the config.json file.

import json
import os


class ConfigService:
    """
    Class responsible for reading and writing the config.json file.
    """

    def __init__(self, config_file='config.json'):
        """
        Initialize a ConfigService instance.

        :param config_file: Path to the configuration file.
        :type config_file: str
        """
        self.config_file = config_file
        self.config_data = self.load_config()

    def reload(self):
        """
        Reload the configuration data from the file.
        """
        self.config_data = self.load_config()

    def load_config(self):
        """
        Load the configuration data from the file.

        :return: Configuration data.
        :rtype: dict
        """
        if os.path.exists(self.config_file):
            if os.path.getsize(self.config_file) > 0:
                with open(self.config_file, 'r') as file:
                    return json.load(file)
            else:
                self.initialize_config()
                return {}
        else:
            self.initialize_config()
            return {}

    def initialize_config(self):
        """
        Initialize the configuration file with default values.
        """
        with open(self.config_file, 'w') as file:
            json.dump({'cred_path': '', 'db_url': ''}, file, indent=4)

    def save_config(self):
        """
        Save the current configuration data to the file.
        """
        with open(self.config_file, 'w') as file:
            json.dump(self.config_data, file, indent=4)
        self.reload()

    def get_cred_path(self):
        """
        Get the credential path from the configuration data.

        :return: Credential path.
        :rtype: str
        """
        return self.config_data.get('cred_path', '')

    def set_cred_path(self, cred_path):
        """
        Set the credential path in the configuration data.

        :param cred_path: Path to the credentials.
        :type cred_path: str
        """
        self.config_data['cred_path'] = cred_path
        self.save_config()

    def get_db_url(self):
        """
        Get the database URL from the configuration data.

        :return: Database URL.
        :rtype: str
        """
        self.reload()
        return self.config_data.get('db_url', '')

    def set_db_url(self, db_url):
        """
        Set the database URL in the configuration data.

        :param db_url: URL of the database.
        :type db_url: str
        """
        self.config_data['db_url'] = db_url
        self.save_config()

    def get_default_account_book(self) -> str:
        """
        Get the default account book name from the configuration data.

        :return: Default account book name.
        :rtype: str
        """
        self.reload()
        return self.config_data.get('default_account_book', '')

    def set_default_account_book(self, account_book_name):
        """
        Set the default account book name in the configuration data.

        :param account_book_name: Name of the default account book.
        :type account_book_name: str
        """
        self.config_data['default_account_book'] = account_book_name
        self.save_config()
