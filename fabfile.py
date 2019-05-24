from fabric.api import *
from fabric.contrib import files
from fabric.contrib.files import exists
from fabric.colors import green, red, blue
# from fabric.contrib import project
import time
import json
import os
import zipfile

if os.name != 'nt':
    env.use_ssh_config = True
    env.hosts = ['server']
    env.user = env.local_user

PROJECT_NAME = 'ac_ufa_site'
PROJECT_FOLDER = '/home/{}/{}'.format(env.user, PROJECT_NAME)
env.activate = 'source /home/{}/django2/bin/activate'.format(env.user)

def backup_data():
    if exists(PROJECT_FOLDER):
        with cd(PROJECT_FOLDER):
            with prefix(env.activate):
                run('python3 manage.py dumpdata --exclude=auth --exclude=contenttypes > {}_dump.json'.format(PROJECT_NAME))
            run('zip -r media.zip media/')
        get('{}/{}_dump.json'.format(PROJECT_FOLDER, PROJECT_NAME))
        get('{}/media.zip'.format(PROJECT_FOLDER))
    else:
        print(green('folder does not exist'))

def commit():
    local('git add .')
    local('git commit -m "{}"'.format(time.ctime()))

def push():
    local('git push -u origin master')
