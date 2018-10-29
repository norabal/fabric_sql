import os


def adjust_for_expanduser(dir_path):
    """replace '~' as $HOME path for python os module"""
    if dir_path.startswith('~/'):
        return dir_path.replace('~', os.path.expanduser('~'), 1)
    else:
        return dir_path
