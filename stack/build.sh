#!/bin/bash

llama stack build --config build.yaml --image-type container --image-name my-llama-stack

docker tag my-llama-stack:0.2.4 registry.home.glroland.com/llama/stack:1

# docker push registry.home.glroland.com/llama/stack:1
