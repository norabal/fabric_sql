import os
from configparser import ConfigParser


def adjust_for_expanduser(dir_path: str) -> str:
    """replace '~' as $HOME path for python os module"""
    if dir_path.startswith('~/'):
        return dir_path.replace('~', os.path.expanduser('~'), 1)
    else:
        return dir_path


def get_config(file_path: str) -> ConfigParser:
    """read config file"""
    config = ConfigParser()
    config.read(file_path, 'UTF-8')

    return config
