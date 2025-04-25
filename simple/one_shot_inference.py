import os
from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger

ENV_LLAMA_STACK_HOST = "LLAMA_STACK_HOST"
ENV_LLAMA_STACK_PORT = "LLAMA_STACK_PORT"
ENV_LLAMA_STACK_MODEL = "LLAMA_STACK_MODEL"

def main():
    # gather configuration
    llama_stack_host = os.environ[ENV_LLAMA_STACK_HOST]
    llama_stack_port = os.environ[ENV_LLAMA_STACK_PORT]
    llama_stack_url = f"http://{llama_stack_host}:{llama_stack_port}"
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
    for model in llama_stack_client.models():
        if model.identifier == llama_stack_model_name:
            llama_stack_model = model
            break
    if llama_stack_model is None:
        print("Model Not Found!")
        return

    agent = Agent(
        llama_stack_client,
        model=llama_stack_model,
        instructions="You are a helpful assistance",
#        tools=["builtin::websearch"],
#        input_shields=available_shields,
#        output_shields=available_shields,
        enable_session_persistence=False,
        sampling_params={
            "strategy": {"type": "top_p", "temperature": 1.0, "top_p": 0.9},
            },    
        )
    user_prompts = [
        "What are the capitals of each major european country?",
    ]

    session_id = agent.create_session("test-session")
    for prompt in user_prompts:
        print(f"User> {prompt}")
        response = agent.create_turn(
            messages=[{"role": "user", "content": prompt}],
            session_id=session_id,
        )

        for log in AgentEventLogger().log(response):
            log.print()



    pass

if __name__ == "__main__":
    main()
