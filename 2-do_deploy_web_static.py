#!/usr/bin/python3
"""Distributes an archive to the web servers."""
from fabric.api import env, run, put
import os

env.hosts = ['100.26.170.206', '34.202.159.66']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        print(f"Error: Archive '{archive_path}' not found.")
        return False

    try:
        put(archive_path, '/tmp/')

        archive_filename = os.path.basename(archive_path)
        release_folder = f'/data/web_static/releases/{archive_filename.split(".")[0]}'
        run(f"mkdir -p {release_folder}")
        run(f"tar -xzf /tmp/{archive_filename} -C {release_folder}")

        # Remove the uploaded archive from the /tmp/ directory
        run(f"rm /tmp/{archive_filename}")

        # Create or update the symbolic link to the new release
        current_link = '/data/web_static/current'
        run(f"rm -f {current_link}")
        run(f"ln -s {release_folder} {current_link}")

        print("New version deployed successfully.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
