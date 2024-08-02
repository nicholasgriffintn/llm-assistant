from .config import ollama_options, text_to_image_model_name
from .helpers import logger
from .functions.generate_image import generate_image

def image( source ):
    """
    Generate an image using the Ollama API.

    Args:
        source (str): The prompt to generate an image from.
    
    Returns:
        str: The generated image.
    """

    try:
        prompt = source
        if prompt is None:
            return
        
        image = generate_image( prompt, ollama_options, text_to_image_model_name )

        if image is None:
            return ""
        
        return image
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return
