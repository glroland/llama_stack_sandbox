import os
from llama_stack_client import LlamaStackClient, LlamaStackClient, Agent, AgentEventLogger
from llama_stack_client.lib.agents.client_tool import client_tool
from llama_stack_client.types.shared_params.agent_config import ToolConfig

ENV_LLAMA_STACK_URL = "LLAMA_STACK_URL"
ENV_LLAMA_STACK_MODEL = "LLAMA_STACK_MODEL"

@client_tool
def calculator(x: float, y: float, operation: str) -> dict:
    """Simple calculator tool that performs basic math operations.

    :param x: First number to perform operation on
    :param y: Second number to perform operation on
    :param operation: Mathematical operation to perform ('add', 'subtract', 'multiply', 'divide')
    :returns: Dictionary containing success status and result or error message
    """
    try:
        if operation == "add":
            result = float(x) + float(y)
        elif operation == "subtract":
            result = float(x) - float(y)
        elif operation == "multiply":
            result = float(x) * float(y)
        elif operation == "divide":
            if float(y) == 0:
                return {"success": False, "error": "Cannot divide by zero"}
            result = float(x) / float(y)
        else:
            return {"success": False, "error": "Invalid operation"}

        return {"success": True, "result": result}
    except Exception as e:
        print(f"Calculator error: {str(e)}")
        return {"success": False, "error": str(e)}

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
        tools=[calculator],
        tool_config=ToolConfig(tool_choice = "auto"),
    )

    # Create a session
    session_id = agent.create_session(session_name="My conversation")

    user_prompts = [
        "What are the capitals of each major european country?",
        "hello world, write me a 2 sentence poem about the moon",
        "What is 9 * 7?",
        "What is 2 * 2 * 2?"
    ]

    # send chat completion request
    print ("Sending agent requests...")
    for prompt in user_prompts:
        # Display Prompt
        print ("user> ", prompt)
    
        # Send request
        response = agent.create_turn(
            session_id=session_id,
            messages=[{"role":"user", "content":prompt}],
            stream=True
        )

        # Display Response (streaming)
        for log in AgentEventLogger().log(response):
            log.print()

if __name__ == "__main__":
    main()
