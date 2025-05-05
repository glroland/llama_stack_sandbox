import os
from llama_stack_client import LlamaStackClient, LlamaStackClient, Agent, AgentEventLogger

ENV_LLAMA_STACK_URL = "LLAMA_STACK_URL"
ENV_LLAMA_STACK_MODEL = "LLAMA_STACK_MODEL"

def main():
    # gather configuration
    llama_stack_url = os.environ[ENV_LLAMA_STACK_URL]
    print ("LLama Stack URL: ", llama_stack_url)
    llama_stack_model_name = os.environ[ENV_LLAMA_STACK_MODEL]
    print ("LLama Stack Model: ", llama_stack_model_name)

    # connect to llama stack environment
    print ("Connecting to Llama Stack....")
    llama_stack_client = LlamaStackClient(
        base_url=llama_stack_url,
    )
    print ("Connected")

    # find model matching name
    print ("Finding Requested LLama Model...")
    llama_stack_model = None
    for model in llama_stack_client.models.list():
        if model.identifier == llama_stack_model_name:
            llama_stack_model = model
            break
    if llama_stack_model is None:
        print("Model Not Found!")
        return

    # Create the agent
    agent = Agent(
        llama_stack_client,
        model=llama_stack_model.identifier,
        instructions="You are a helpful assistant that can use tools to answer questions.",
        tools=[],
    )

    # Create a session
    session_id = agent.create_session(session_name="My conversation")

    user_prompts = [
        "What are the capitals of each major european country?",
        "hello world, write me a 2 sentence poem about the moon",
    ]

    # send chat completion request
    print ("Sending agent requests...")
    for prompt in user_prompts:
    
        # Send request
        response = agent.create_turn(
            session_id=session_id,
            messages=[{"role":"user", "content":prompt}],
            stream=True
        )
        for log in AgentEventLogger().log(response):
            log.print()

if __name__ == "__main__":
    main()
