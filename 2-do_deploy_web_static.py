#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import put, run, env, local
from os.path import exists, basename, splitext
from datetime import datetime

env.hosts = ['54.91.97.107', '3.95.175.50']
env.user = 'ubuntu'  # Set your SSH username here
env.key_filename = 'my_ssh_private_key'  # Set your SSH private key path here


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        # Extract filename and directory name
        file_name = basename(archive_path)
        base_name = splitext(file_name)[0]
        release_path = "/data/web_static/releases/{}".format(base_name)
        tmp_path = "/tmp/{}".format(file_name)

        # Upload the archive to /tmp/
        put(archive_path, tmp_path)

        # Create release directory
        run("mkdir -p {}".format(release_path))

        # Uncompress the archive
        run("tar -xzf {} -C {}".format(tmp_path, release_path))

        # Remove the archive
        run("rm {}".format(tmp_path))

        # Move files from web_static subdirectory
        run("mv {}/web_static/* {}".format(release_path, release_path))

        # Remove the empty web_static directory
        run("rm -rf {}/web_static".format(release_path))

        # Remove current symlink
        run("rm -rf /data/web_static/current")

        # Create new symlink
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False
