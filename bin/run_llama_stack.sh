#!/bin/bash

export LLAMA_PATH=C:\Users\glrol\.llama
export LLAMA_STACK_PORT=8321
export LLAMA_MODEL=meta-llama/Llama-3.2-11B-Vision-Instruct

echo llama stack build --template meta-reference-gpu --image-type conda

llama stack run ~/.llama/distributions/meta-reference-gpu/meta-reference-gpu-run.yaml --port $LLAMA_STACK_PORT --env INFERENCE_MODEL=$LLAMA_MODEL

