#!/usr/bin/env bash
commit_sha=$(git rev-parse HEAD)
repo_url="registry.scavenger.news/scavenger_blog"

dir_path=$(cd $(dirname "${BASH_SOURCE:-$0}") && pwd)

docker build --build-arg requirements="requirements.in requirements-prod.in" -t $repo_url:$commit_sha -f $dir_path/../Minimal.Dockerfile $dir_path/../

AWS_PROFILE=zilla docker push $repo_url:$commit_sha
