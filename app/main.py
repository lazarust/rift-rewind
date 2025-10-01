import logging

import gradio as gr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def answer(message, history):
    return f"History Len: {len(history)}\n Message: {message}"


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
