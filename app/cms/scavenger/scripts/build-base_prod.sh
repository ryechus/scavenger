#!/usr/bin/env bash
has_changes=$(git diff --compact-summary | grep -E ".*Base.Dockerfile | .*requirements(-prod)?\.in")
last_exit=$(echo $?)

if [ $last_exit -eq 0 ]; then
    echo "Can't build: commit changes to dependency files"
    exit
fi

commit_sha=$(git rev-parse --short HEAD)
repo_url="ryechus/scavenger-wagtail"
image_tag="base-$commit_sha"
full_image_str=$repo_url:$image_tag

dir_path=$(cd $(dirname "${BASH_SOURCE:-$0}") && pwd)

docker build --build-arg requirements="requirements.in requirements-prod.in" -t $full_image_str \
-f $dir_path/../Base.Dockerfile $dir_path/../

AWS_PROFILE=zilla docker push $full_image_str
