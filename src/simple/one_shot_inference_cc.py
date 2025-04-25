import os
from llama_stack_client import LlamaStackClient, LlamaStackClient
from llama_stack_client.types import UserMessage

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
    for model in llama_stack_client.models.list():
        if model.identifier == llama_stack_model_name:
            llama_stack_model = model
            break
    if llama_stack_model is None:
        print("Model Not Found!")
        return

    user_prompts = [
        "What are the capitals of each major european country?",
        "hello world, write me a 2 sentence poem about the moon",
    ]

    # send chat completion request
    print ("Sending chat completion request...")
    for prompt in user_prompts:
        print ("User> ", prompt)
        response = llama_stack_client.inference.chat_completion(
            messages=[
                UserMessage(
                    content=prompt,
                    role="user",
                ),
            ],
            model_id=llama_stack_model.identifier,
            stream=False,
        )
        #print (response)
        print (response.completion_message.content)



if __name__ == "__main__":
    main()


