#!/bin/bash

set -eu

PULSEAUDIO_COOKIE_TMP_MOUNT_PATH=/tmp/pulse
USER_NAME=user

useradd -u "${HOST_UID}" -o -m "${USER_NAME}"
groupmod -g "${HOST_GID}" "${USER_NAME}"

gosu "${USER_NAME}" mkdir -p "/home/${USER_NAME}/.config/pulse"
cp -r "${PULSEAUDIO_TMP_MOUNT_PATH}" "/home/${USER_NAME}/.config/"

gosu "${USER_NAME}" $@

