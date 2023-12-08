#!/usr/bin/python3
"""distributes an archive to your web servers"""
import os
from fabric.api import env, run, put

env.hosts = ['100.26.170.206', '34.202.159.66']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    try:
        # Check if the archive file exists
        if not os.path.exists(archive_path):
            raise FileNotFoundError(
                f"The archive file {archive_path} does not exist.")

        # Extract necessary information from the archive path
        file_name = archive_path.split("/")[-1]
        archive_name = file_name.split(".")[0]
        release_path = "/data/web_static/releases/"

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create a new release directory
        run('mkdir -p {}{}/'.format(release_path, archive_name))

        # Extract the contents of the archive to the release directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(
            file_name, release_path, archive_name))

        # Remove the uploaded archive from /tmp/
        run('rm /tmp/{}'.format(file_name))

        # Move the contents to the parent directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(
            release_path, archive_name))

        # Remove the web_static directory within the release directory
        run('rm -rf {}{}/web_static'.format(release_path, archive_name))

        # Remove the existing /data/web_static/current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the latest release
        run('ln -s {}{}/ /data/web_static/current'.format(
            release_path, archive_name))

        print("New version deployed successfully.")
        return True

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Error during deployment: {e}")
        return False
