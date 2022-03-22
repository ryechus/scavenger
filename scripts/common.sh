#!/usr/bin/env bash
echo $1
environment="scavenger.settings.local"

if [ "" != "$1" ]; then
    environment=$1
fi
