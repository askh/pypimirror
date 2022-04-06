#!/usr/bin/env python3

import argparse
import os.path
import subprocess
from dotenv import dotenv_values
import yaml

arg_parser = argparse.ArgumentParser(description="The script for start devpi-server")
arg_parser.add_argument(
    '-d',
    '--data-dir',
    type=str,
    default = '/var/local/devpisrv',
    help = 'Path to the data directory'
)
args = arg_parser.parse_args()

server_dir = os.path.join(args.data_dir, "server")
config_dir = os.path.join(args.data_dir, "config")
env_file = os.path.join(config_dir, ".env")
config_file = os.path.join(config_dir, "devpi.conf")

if not os.path.exists(config_file):
    config_data = {
        'devpi-server': {
            'serverdir': os.path.abspath(server_dir),
            'host': '0.0.0.0',
            'restrict-modify': 'root'
        }
    }    
    if os.path.isfile(env_file):
        env_config_values = dotenv_values(env_file)
        if 'ROOT_PASSWORD' in env_config_values.keys():
            config_data['devpi-server']['root-passwd'] = \
                env_config_values['ROOT_PASSWORD']
    with open(config_file, 'w') as file:
        yaml.dump(config_data, file)

if not os.path.exists(os.path.join(server_dir, ".nodeinfo")):
    subprocess.run(
        args=[
            'devpi-init',
            '--serverdir', server_dir,
            '--configfile', config_file
        ],
        check=True
    )

subprocess.run(
    args=[
        'devpi-server',
        '--configfile', config_file
    ],
    check=True
)

