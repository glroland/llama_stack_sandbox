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
    llama_stack_model = os.environ[ENV_LLAMA_STACK_MODEL]
    print ("LLama Stack Model: ", llama_stack_model)

    # connect to llama stack environment
    print ("Connecting to Llama Stack....")
    llama_stack_client = LlamaStackClient(
        base_url=llama_stack_url,
    )
    print ("Connected")

    agent = Agent(
        llama_stack_client,
        model=llama_stack_model,
        instructions="",
#        tools=["builtin::websearch"],
#        input_shields=available_shields,
#        output_shields=available_shields,
        enable_session_persistence=False,
    )
    user_prompts = [
        "Hello",
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
