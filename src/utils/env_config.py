import configparser
import os.path


class EnvConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        my_path = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(my_path, "gearmood.ini")
        self.config.read(config_path)

    def get_section_items(self, section):
        return self.config.items(section)

    def get_value(self, section, option):
        return self.config.get(section, option)
