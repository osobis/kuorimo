import os
from os.path import expanduser


def get_home_dir():
    if os.name == 'nt':
        return 'C:\\'
    return expanduser("~")
