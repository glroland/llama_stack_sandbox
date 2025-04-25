@echo off

set LLAMA_PATH=C:\Users\glrol\.llama
set LLAMA_STACK_PORT=8321
set LLAMA_MODEL=meta-llama/Llama-3.2-11B-Vision-Instruct

echo llama stack build --template meta-reference-gpu --image-type conda

echo llama stack run distributions/meta-reference-gpu/run.yaml --port %LLAMA_STACK_PORT% --env INFERENCE_MODEL=%LLAMA_MODEL%
