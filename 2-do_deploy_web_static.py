#!/usr/bin/python3
"""
Fabric script to deploy web_static and configure Nginx
"""

from fabric.api import *
from os.path import exists
import os

env.hosts = ["54.175.105.22", "54.175.110.39"]
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    Deploys an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        name_no_ext = filename.split('.')[0]
        release_dir = f"/data/web_static/releases/{name_no_ext}"
        tmp_path = f"/tmp/{filename}"

        # Upload the archive to /tmp/
        put(archive_path, tmp_path)

        # Create release folder and extract
        run(f"mkdir -p {release_dir}")
        run(f"tar -xzf {tmp_path} -C {release_dir}")
        run(f"rm {tmp_path}")

        # Move contents from web_static/* to release_dir
        run(f"mv {release_dir}/web_static/* {release_dir}/")
        run(f"rm -rf {release_dir}/web_static")

        # Remove old symlink and create new one
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_dir} /data/web_static/current")

        # Configure Nginx if needed
        configure_nginx()

        print("New version deployed!")
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False


def configure_nginx():
    """
    One-time setup: add /hbnb_static/ location to Nginx config if not present
    """
    location_block = """
    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
        try_files $uri $uri/ =404;
    }
    """

    # Check if /hbnb_static is already configured
    result = run("grep '/hbnb_static/' /etc/nginx/sites-available/default", warn_only=True)

    if result.failed:
        # Add location block right after 'server_name _;'
        escaped_block = location_block.replace('\n', '\\n').replace('"', '\\"')
        run(f'sudo sed -i "/server_name _;/a {escaped_block}" /etc/nginx/sites-available/default')
        run("sudo service nginx restart")
