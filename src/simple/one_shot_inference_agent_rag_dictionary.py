import os
import requests
import uuid
from llama_stack_client import LlamaStackClient, LlamaStackClient, Agent, AgentEventLogger, RAGDocument

ENV_LLAMA_STACK_URL = "LLAMA_STACK_URL"
ENV_LLAMA_STACK_MODEL = "LLAMA_STACK_MODEL"
ENV_EMBEDDING_MODEL = "EMBEDDING_MODEL"

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

    # Register a vector database
    vector_db_id = "one_shot_inference_agent_rag"
    llama_stack_client.vector_dbs.register(
        vector_db_id=vector_db_id,
        embedding_model=embedding_model_name,
        embedding_dimension=384,
        provider_id="faiss",
    )

    # Create the agent
    agent = Agent(
        llama_stack_client,
        model=llama_stack_model.identifier,
        instructions="You are a helpful assistant that can use tools to answer questions.",
        tools=["builtin::rag"],
    )

    # Create a session
    session_id = agent.create_session(session_name="My conversation")

    # download dictionary file
    dictionary_file = "../../content/Oxford English Dictionary.txt"
    if not os.path.isfile(dictionary_file):
        raise ValueError("Dictionary file not found!")

    # load file
    print ("Reading dictionary file...")
    dictionary_data = None
    with open(dictionary_file, "r") as file:
        dictionary_data = str(file.read())
    print ("Done")
    if dictionary_data is None:
        raise ValueError("No dictionary data found!")

    # splitting lines into groups
    print ("Creating groups of dictionary entries from data set...")
    dictionary_lines = dictionary_data.splitlines()
    dictionary_groups = chunk_array(dictionary_lines, 800)
    print ("Done")

    # Chunk it by line
    print ("Chunking content...")
    chunks = []
    document_id = 0
    for group in dictionary_groups:
        content = "".join(group)
        document_id += 1
        if len(content) > 0:
            chunk = {
                "content": content,
                "mime_type": "text/plain",
                "metadata": {
                    "document_id": f"doc_{document_id}",
                    "token_count": token_count,
                },
            }
            chunks.append(chunk)
    print ("Done")

    # Import content
    print ("Importing dictionary content into database...")
    llama_stack_client.vector_io.insert(vector_db_id=vector_db_id, chunks=chunks)
    print ("Done")

    user_prompts = [
        "What is a basketball?",
        "How many legs does an arachnid have?",
    ]

    # send RAG inquiries
    print ("Sending agent requests...")
    for user_prompt in user_prompts:

        # Query documents
        results = llama_stack_client.tool_runtime.rag_tool.query(
            vector_db_ids=[vector_db_id],
            content=user_prompt,
        )
        print (results)


if __name__ == "__main__":
    main()
