#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

from fabric.api import *
from os.path import exists
import os

env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with actual IPs
env.user = 'ubuntu'  # Replace with your username if different


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of web server
        put(archive_path, "/tmp/")

        # Get archive filename without extension
        archive_filename = os.path.basename(archive_path)
        archive_name = archive_filename.split('.')[0]

        # Create target directory
        releases_path = "/data/web_static/releases/{}/".format(archive_name)
        run("mkdir -p {}".format(releases_path))

        # Uncompress archive to target directory
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, releases_path))

        # Delete archive from web server
        run("rm /tmp/{}".format(archive_filename))

        # Move contents to proper location
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))

        # Delete existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link
        run("ln -s {} /data/web_static/current".format(releases_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed:", str(e))
        return False
