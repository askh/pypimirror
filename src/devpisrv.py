#!/usr/bin/env python3

import argparse
import os.path
import subprocess
from dotenv import dotenv_values
import yaml

DEFAULT_REQUEST_TIMEOUT_SEC = 10

arg_parser = argparse.ArgumentParser(description="The script for start devpi-server")
arg_parser.add_argument(
    '-d',
    '--data-dir',
    type=str,
    default='/var/local/devpisrv',
    help='Path to the data directory'
)
arg_parser.add_argument(
    '-w',
    '--overwrite-config',
    action='store_true',
    default=False,
    help='Overwrite the config file if exists')
args = arg_parser.parse_args()

server_dir = os.path.join(args.data_dir, "server")
config_dir = os.path.join(args.data_dir, "config")
env_file = os.path.join(config_dir, ".env")
config_file = os.path.join(config_dir, "devpi.conf")

if not(os.path.exists(args.data_dir) and os.path.isdir(args.data_dir)):
    sys.exit(f"The data directory {args.data_dir} not available.")
for subdir_path in [server_dir, config_dir]:
    if not os.path.exists(subdir_path):
        os.mkdir(subdir_path, mode=0o770)

if not os.path.exists(config_file) or args.overwrite_config:
    env_config_values = dotenv_values(env_file) if os.path.isfile(env_file) else { }

    config_data = {
        'devpi-server': {
            'serverdir': os.path.abspath(server_dir),
            'host': '0.0.0.0',
            'restrict-modify': 'root',
            'request-timeout': int(env_config_values.get('REQUEST_TIMEOUT_SEC') or \
                                   DEFAULT_REQUEST_TIMEOUT_SEC)
        }
    }
    
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

