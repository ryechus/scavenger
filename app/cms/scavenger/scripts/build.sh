#!/usr/bin/env bash
commit_sha=$(git rev-parse HEAD)
repo_url="188863028714.dkr.ecr.us-west-1.amazonaws.com/scavenger_blog"

docker build -t $repo_url:$commit_sha -f Minimal.Dockerfile .

AWS_PROFILE=zilla docker push $repo_url:$commit_sha
