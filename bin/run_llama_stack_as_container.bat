@echo off

set LLAMA_PATH=C:\Users\glrol\.llama
set DISTRO=llamastack/distribution-meta-reference-gpu:latest
set LLAMA_STACK_PORT=8321
rem set LLAMA_MODEL=meta-llama/Llama-3.1-8B-Instruct
set LLAMA_MODEL=meta-llama/Llama-3.2-11B-Vision-Instruct

docker pull %DISTRO%

docker run --rm --gpus all -d -p %LLAMA_STACK_PORT%:%LLAMA_STACK_PORT% -v %LLAMA_PATH%:/root/.llama %DISTRO% --port %LLAMA_STACK_PORT% --env INFERENCE_MODEL=%LLAMA_MODEL%

rem docker run --gpus all -it -p %LLAMA_STACK_PORT%:%LLAMA_STACK_PORT% -v %LLAMA_PATH%:/root/.llama %DISTRO% --port %LLAMA_STACK_PORT% --env INFERENCE_MODEL=%LLAMA_MODEL%

rem docker run -it -p %LLAMA_STACK_PORT%:%LLAMA_STACK_PORT% -v %LLAMA_PATH%:/root/.llama %DISTRO% --port %LLAMA_STACK_PORT% --env INFERENCE_MODEL=meta-llama/Llama3.1-8B-Instruct --env SAFETY_MODEL=meta-llama/Llama-Guard-3-8B


