LLAMA_STACK_HOST := envision
LLAMA_STACK_PORT := 8321
LLAMA_STACK_MODEL := meta-llama/Llama-3.2-11B-Vision-Instruct

MCP_IMAGE := registry.home.glroland.com/llama/calc-mcp-server
MCP_IMAGE_TAG := 10

install:
	pip install -r requirements.txt

run:
	cd src/simple && LLAMA_STACK_HOST=$(LLAMA_STACK_HOST) LLAMA_STACK_PORT=$(LLAMA_STACK_PORT) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) python one_shot_inference_agent_w_mcp.py

run.all:
	cd src/simple && LLAMA_STACK_HOST=$(LLAMA_STACK_HOST) LLAMA_STACK_PORT=$(LLAMA_STACK_PORT) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) python one_shot_inference_cc.py
	cd src/simple && LLAMA_STACK_HOST=$(LLAMA_STACK_HOST) LLAMA_STACK_PORT=$(LLAMA_STACK_PORT) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) python one_shot_inference_agent.py
	cd src/simple && LLAMA_STACK_HOST=$(LLAMA_STACK_HOST) LLAMA_STACK_PORT=$(LLAMA_STACK_PORT) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) python one_shot_inference_agent_w_tool.py

run.mcp:
	cd calc_mcp_server/src && python calc_mcp_server.py

publish:
	cd calc_mcp_server && podman build . --platform=linux/amd64 -t $(MCP_IMAGE):latest
	podman tag $(MCP_IMAGE):latest $(MCP_IMAGE):$(MCP_IMAGE_TAG)
	podman push $(MCP_IMAGE):$(MCP_IMAGE_TAG)
