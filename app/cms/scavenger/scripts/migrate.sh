#!/usr/bin/env bash

DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/common.sh"

docker compose run -e DJANGO_SETTINGS_MODULE=$environment --rm django ./manage.py migrate
