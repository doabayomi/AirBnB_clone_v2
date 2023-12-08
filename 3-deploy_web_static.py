#!/usr/bin/python3
"""A Fabric Script to deploy archive to the web servers"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['54.83.175.223', '100.25.136.195']
env.user = "ubuntu"

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

@task
def do_deploy(archive_path):
    """Deploys a .tgz archive into the servers

    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    archive_filename = os.path.splitext(os.path.basename(archive_path))[0]

    local_file_path = archive_path
    remote_file_path = "/tmp/" + os.path.basename(archive_path)

    data_path = "/data/web_static/releases/" + archive_filename
    upload = put(local_file_path, remote_file_path)
    if upload.failed:
        return False

    run("mkdir -p " + data_path)
    run("tar -xzf " + remote_file_path + " -C " + data_path)
    run("rm " + remote_file_path)

    with cd(data_path):
        run("mv web_static/* .")
        run("rm -rf web_static")

    current_path = "/data/web_static/current"
    run("rm -rf " + current_path)
    run("ln -s " + data_path + " " + current_path)

    return True
