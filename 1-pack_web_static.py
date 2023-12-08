#!/usr/bin/python3
"""A Fabric Script that generates a tar .gz archive"""
from fabric.api import *
from datetime import datetime


@task
def do_pack():
    """Creates a .tgz archive from /web_static/

    Returns:
        str: The path to the archive if successful, None, If failed
    """
    today = datetime.now()

    date_code = "{year}".format(year=today.year)
    date_code += "{month:02d}".format(month=today.month)
    date_code += "{day:02d}".format(day=today.day)
    date_code += "{hour:02d}".format(hour=today.hour)
    date_code += "{minute:02d}".format(minute=today.minute)
    date_code += "{second:02d}".format(second=today.second)

    """Creating filename"""
    path = "versions/web_static_" + date_code + ".tgz"
    local("mkdir -p versions")
    result = local("tar -cvzf " + path + " web_static")

    if result.failed:
        return None
    return path
