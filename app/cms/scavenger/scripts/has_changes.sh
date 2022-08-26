#!/usr/bin/env bash
has_changes=$(git show --name-status --pretty=oneline -1 HEAD | grep -E "app/cms/scavenger/.*\.py|app/cms/scavenger/.*\.html")
last_exit=$(echo $?)

if [ $last_exit -eq 0 ]; then
    echo "Changes to CMS app source code exist"
    exit 0
fi

exit 1
