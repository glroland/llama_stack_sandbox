import os
import uuid
from llama_stack_client import LlamaStackClient, LlamaStackClient, Agent
from llama_stack_client.types import Document

ENV_LLAMA_STACK_URL = "LLAMA_STACK_URL"
ENV_LLAMA_STACK_MODEL = "LLAMA_STACK_MODEL"
ENV_EMBEDDING_MODEL = "EMBEDDING_MODEL"

RAG_PROMPT_TESTS = [
    {
        "input_query": "What precision formats does torchtune support?",
        "expected_answer": "Torchtune supports two data types for precision: fp32 (full-precision) which uses 4 bytes per model and optimizer parameter, and bfloat16 (half-precision) which uses 2 bytes per model and optimizer parameter."
    },
    {
        "input_query": "What does DoRA stand for in torchtune?",
        "expected_answer": "Weight-Decomposed Low-Rank Adaptation"
    },
    {
        "input_query": "How does the CPUOffloadOptimizer reduce GPU memory usage?",
        "expected_answer": "The CPUOffloadOptimizer reduces GPU memory usage by keeping optimizer states on CPU and performing optimizer steps on CPU. It can also optionally offload gradients to CPU by using offload_gradients=True"
    },
    {
        "input_query": "How do I ensure only LoRA parameters are trainable when fine-tuning?",
        "expected_answer": "You can set only LoRA parameters to trainable using torchtune's utility functions: first fetch all LoRA parameters with lora_params = get_adapter_params(lora_model), then set them as trainable with set_trainable_params(lora_model, lora_params). The LoRA recipe handles this automatically."
    }
]

def chunk_array(arr, chunk_size):
    return [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

def main():
    # gather configuration
    llama_stack_url = os.environ[ENV_LLAMA_STACK_URL]
    print ("LLama Stack URL: ", llama_stack_url)
    llama_stack_model_name = os.environ[ENV_LLAMA_STACK_MODEL]
    print ("LLama Stack Model: ", llama_stack_model_name)
    embedding_model_name = os.environ[ENV_EMBEDDING_MODEL]
    print ("Embedding Model: ", embedding_model_name)

    # connect to llama stack environment
    print ("Connecting to Llama Stack....")
    llama_stack_client = LlamaStackClient(
        base_url=llama_stack_url,
    )
    print ("Connected")

    # find model matching name
    print ("Finding Requested LLama Model...", llama_stack_client.models.list())
    llama_stack_model = None
    for model in llama_stack_client.models.list():
        if model.identifier == llama_stack_model_name:
            llama_stack_model = model
            break
    if llama_stack_model is None:
        print("Model Not Found!")
        return

    # get a list of registered vector databases
    vector_providers = [
        provider for provider in llama_stack_client.providers.list() if provider.api == "vector_io"
    ]
    if not vector_providers:
        print("No available vector_io providers. Exiting.")
        return
    print ("Registered Vector Databases: ", vector_providers)

    # choose vector store
    selected_vector_provider = vector_providers[0]
    print ("Selected Vector Store: ", selected_vector_provider)

    # laod documents
    urls = [
        "memory_optimizations.rst",
        "chat.rst",
        "llama3.rst",
        "qat_finetune.rst",
        "lora_finetune.rst",
    ]
    documents = [
        Document(
            document_id=f"num-{i}",
            content=f"https://raw.githubusercontent.com/pytorch/torchtune/main/docs/source/tutorials/{url}",
            mime_type="text/plain",
            metadata={},
        )
        for i, url in enumerate(urls)
    ]

    # register the vector database (each run gets its own database)
    vector_db_id = f"test_vector_db_{uuid.uuid4()}"
    print ("Registering Vector DB:", vector_db_id)
    llama_stack_client.vector_dbs.register(
        vector_db_id=vector_db_id,
        embedding_model="all-MiniLM-L6-v2",
        embedding_dimension=384,
        provider_id=selected_vector_provider.provider_id,
    )
    print ("Database Registered")

    # store all the documents
    print ("Storing all documents...")
    llama_stack_client.tool_runtime.rag_tool.insert(
        documents=documents,
        vector_db_id=vector_db_id,
        chunk_size_in_tokens=512,
    )
    print ("Documents Stored")

    # create agent
    print ("Creating Agent...")
    rag_agent = Agent(
        llama_stack_client,
        model=llama_stack_model_name,
        instructions="You are a helpful assistant that can answer questions about the Torchtune project. You should always use the RAG tool to answer questions.",
        tools=[{
            "name": "builtin::rag",
            "args": {"vector_db_ids": [vector_db_id]},
        }],
    )
    print ("Agent Created")

    # run each example
    for example in RAG_PROMPT_TESTS:
        print ("EXAMPLE...")
        print()
        print(f"Question: {example['input_query']}")
        print()
        print(f"EXPECTED Response: {example['expected_answer']}")
        print()

        rag_session_id = rag_agent.create_session(session_name=f"rag_session_{uuid.uuid4()}")
        response = rag_agent.create_turn(
            messages=[
                {
                    "role": "user",
                    "content": example["input_query"]
                }
            ],
            session_id=rag_session_id,
            stream=False
        )
        print(f"ACTUAL Response: {response.output_message.content}")
        print()
        print ("-------------------------------------------------------------")
        print()

    print ("Complete!")

if __name__ == "__main__":
    main()
