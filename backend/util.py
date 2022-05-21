import os
from datetime import datetime, timezone

def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def get_current_time_ms():
    """ return current time in UTC in ms """
    return get_current_time().timestamp() * 1000

def get_current_time():
    """ return current datetime in UTC """
    return datetime.now(timezone.utc)

