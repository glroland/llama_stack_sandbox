LLAMA_STACK_HOST := envision
LLAMA_STACK_PORT := 8321
LLAMA_STACK_MODEL := meta-llama/Llama-3.2-11B-Vision-Instruct

install:
	pip install -r requirements.txt

run:
	cd src/simple && LLAMA_STACK_HOST=$(LLAMA_STACK_HOST) LLAMA_STACK_PORT=$(LLAMA_STACK_PORT) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) python one_shot_inference_agent_w_mcp.py

run.all:
	cd src/simple && LLAMA_STACK_HOST=$(LLAMA_STACK_HOST) LLAMA_STACK_PORT=$(LLAMA_STACK_PORT) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) python one_shot_inference_cc.py
	cd src/simple && LLAMA_STACK_HOST=$(LLAMA_STACK_HOST) LLAMA_STACK_PORT=$(LLAMA_STACK_PORT) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) python one_shot_inference_agent.py
	cd src/simple && LLAMA_STACK_HOST=$(LLAMA_STACK_HOST) LLAMA_STACK_PORT=$(LLAMA_STACK_PORT) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) python one_shot_inference_agent_w_tool.py

run.mcp:
	cd src/simple && mcp dev calc_mcp_server.py
