#!/bin/bash

SERVER_DIR=/var/local/devpisrv

if [[ ! -f "$SERVER_DIR/.nodeinfo" ]]
then
    devpi-init --serverdir "$SERVER_DIR"
fi

devpi-server --serverdir "$SERVER_DIR" --host 0.0.0.0

