#!/bin/bash

DEFAULT_INSECURE_ROOT_PASSWORD="root"

DATA_DIR=/var/local/devpisrv
SERVER_DIR=${DATA_DIR}/server
INSTALL_DIR=${DATA_DIR}/install
ENV_FILE=${INSTALL_DIR}/.env

if [[ ! -f "$SERVER_DIR/.nodeinfo" ]]
then
    if [[ -f "$ENV_FILE" ]]
    then
        source "$ENV_FILE"
    fi
    INSTALL_ROOT_PASSWORD=${ROOT_PASSWORD:-${DEFAULT_INSECURE_ROOT_PASSWORD}}
    devpi-init --serverdir "$SERVER_DIR" --root-passwd "${INSTALL_ROOT_PASSWORD}"
    rm "${INSTALL_DIR}/*"
fi

devpi-server --serverdir "$SERVER_DIR" --host 0.0.0.0 --restrict-modify root

