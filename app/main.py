import logging

import boto3
import gradio as gr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

model_id = "amazon.nova-micro-v1:0"
client = boto3.client("bedrock-runtime", region_name="us-east-1")


def answer(message, history):
    messages = history.copy()
    print(messages)
    current_message = {"role": "user", "content": [{"text": message}]}
    messages.append(current_message)
    try:
        response = client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )
        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        return str(e)


def main():
    logger.info("Starting Gradio app")
    demo = gr.ChatInterface(
        answer,
        type="messages",
        title="Chatbot",
        description="",
        textbox=gr.Textbox(),
    )

    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
