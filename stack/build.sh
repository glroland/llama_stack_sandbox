#!/bin/bash

llama stack build --config build.yaml --image-type container --image-name my-llama-stack

docker build . --file Dockerfile.run_override -t registry.home.glroland.com/llama/stack:1

# docker push registry.home.glroland.com/llama/stack:1
