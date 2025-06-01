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
    Deploys archive and configures Nginx
    """
    if not exists(archive_path):
        return False

    try:
        # File and directory setup
        filename = os.path.basename(archive_path)
        dirname = filename.split('.')[0]
        releases_path = f"/data/web_static/releases/{dirname}"
        tmp_path = f"/tmp/{filename}"

        # Upload and extract
        put(archive_path, "/tmp/")
        run(f"mkdir -p {releases_path}")
        run(f"tar -xzf {tmp_path} -C {releases_path}")
        run(f"rm {tmp_path}")
        run(f"mv {releases_path}/web_static/* {releases_path}")
        run(f"rm -rf {releases_path}/web_static")

        # Link management
        run("rm -rf /data/web_static/current")
        run(f"ln -s {releases_path} /data/web_static/current")

        # Nginx configuration
        nginx_conf = """
        location /hbnb_static/ {
            alias /data/web_static/current/;
            index index.html;
            try_files $uri $uri/ =404;
        }
        """
        run(f"sudo sed -i '/server_name _;/a {nginx_conf}' /etc/nginx/sites-available/default")
        run("sudo service nginx restart")

        print("New version deployed!")
        return True

    except Exception as e:
        print(f"Deployment failed: {str(e)}")
        return False
