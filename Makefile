LLAMA_STACK_URL := https://my-llama-stack-my-llama-stack.apps.ocp.home.glroland.com
#LLAMA_STACK_URL := https://o1-ollama-llama-stack-ollama-llama.apps.ocp.home.glroland.com
LLAMA_STACK_MODEL := meta-llama/Llama-3.2-11B-Vision-Instruct
EMBEDDING_MODEL := all-MiniLM-L6-v2

MCP_IMAGE := registry.home.glroland.com/llama/calc-mcp-server
MCP_IMAGE_TAG := 10

install:
	pip install -r requirements.txt

run1:
	cd src/simple && LLAMA_STACK_URL=$(LLAMA_STACK_URL) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) EMBEDDING_MODEL=$(EMBEDDING_MODEL) python one_shot_inference_agent_rag_dictionary.py

run2:
	cd src/simple && LLAMA_STACK_URL=$(LLAMA_STACK_URL) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) EMBEDDING_MODEL=$(EMBEDDING_MODEL) python one_shot_inference_agent_rag_techdocs.py

run.all:
	cd src/simple && LLAMA_STACK_URL=$(LLAMA_STACK_URL) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) EMBEDDING_MODEL=$(EMBEDDING_MODEL) python one_shot_inference_cc.py
	cd src/simple && LLAMA_STACK_URL=$(LLAMA_STACK_URL) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) EMBEDDING_MODEL=$(EMBEDDING_MODEL) python one_shot_inference_agent.py
	cd src/simple && LLAMA_STACK_URL=$(LLAMA_STACK_URL) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) EMBEDDING_MODEL=$(EMBEDDING_MODEL) python one_shot_inference_agent_w_tool.py
	cd src/simple && LLAMA_STACK_URL=$(LLAMA_STACK_URL) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) EMBEDDING_MODEL=$(EMBEDDING_MODEL) python one_shot_inference_agent_w_mcp.py
	cd src/simple && LLAMA_STACK_URL=$(LLAMA_STACK_URL) LLAMA_STACK_MODEL=$(LLAMA_STACK_MODEL) EMBEDDING_MODEL=$(EMBEDDING_MODEL) python one_shot_inference_agent_rag.py

run.mcp:
	cd calc_mcp_server/src && python calc_mcp_server.py

publish:
	cd calc_mcp_server && podman build . --platform=linux/amd64 -t $(MCP_IMAGE):latest
	podman tag $(MCP_IMAGE):latest $(MCP_IMAGE):$(MCP_IMAGE_TAG)
	podman push $(MCP_IMAGE):$(MCP_IMAGE_TAG)
