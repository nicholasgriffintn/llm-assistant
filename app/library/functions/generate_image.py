from pathlib import Path
from alive_progress import alive_bar

from ..helpers import generate_text_to_image, logger

def generate_image( prompt, ollama_options, text_to_image_model_name ):
    """
    Generate an image using the LLM.
    
    Args:
        prompt (str): The prompt to generate an image from.
        ollama_options (dict): The options to use for generation.
        model_name (str): The model to use for generation.
        should_stream (bool): Whether to stream the response.
    """

    logger.info(f"Generating image from prompt: {prompt}")
    
    generated = None
    with alive_bar() as bar:
        try:
            generated = generate_text_to_image( 
                prompt,
                ollama_options,
                text_to_image_model_name
            )
            bar()
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return
    
    return generated
