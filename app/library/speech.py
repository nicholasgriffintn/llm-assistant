from .config import ollama_options, speech_recognition_model_name
from .helpers import logger
from .functions.speech_recognition import speech_recognition

def speech( source ):
    """
    Recognise speech using the Ollama API.

    Args:
        source (str): The audio to recognise speech from.
    
    Returns:
        str: The recognised speech.
    """

    try:
        prompt = source
        if prompt is None:
            return
        
        image = speech_recognition( prompt, ollama_options, speech_recognition_model_name )

        if image is None:
            return ""
        
        return image
    except Exception as e:
        logger.error(f"Error recognising speech: {e}")
        return
