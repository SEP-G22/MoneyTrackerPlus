import json
import os

class ConfigService:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
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
        with open(self.config_file, 'w') as file:
            json.dump({'cred_path': '', 'db_url': ''}, file, indent=4)

    def save_config(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.config_data, file, indent=4)

    def get_cred_path(self):
        return self.config_data.get('cred_path', '')

    def set_cred_path(self, cred_path):
        self.config_data['cred_path'] = cred_path
        self.save_config()

    def get_db_url(self):
        return self.config_data.get('db_url', '')

    def set_db_url(self, db_url):
        self.config_data['db_url'] = db_url
        self.save_config()
