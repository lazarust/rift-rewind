import logging

import gradio as gr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def greet(name):
    return f"Hello {name}!"


def main():
    logger.info("Starting Gradio app")
    demo = gr.Interface(fn=greet, inputs="text", outputs="text")
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
