import configparser


def get_config(file_path):
    """read config file"""
    config = configparser.ConfigParser()
    config.read(file_path, 'UTF-8')

    return config
