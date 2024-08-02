from pathlib import Path
from alive_progress import alive_bar

from ..helpers import generate_audio, logger

def speech_recognition( audio, ollama_options, speech_recognition_model_name ):
    """
    Recognise speech using the LLM.
    
    Args:
        audio (str): The audio to recognise speech from.
        ollama_options (dict): The options to use for generation.
        model_name (str): The model to use for generation.
        should_stream (bool): Whether to stream the response.
    """

    logger.info(f"Recognising speech from audio: {audio}")
    
    generated = None
    with alive_bar() as bar:
        try:
            generated = generate_audio( 
                audio,
                ollama_options,
                speech_recognition_model_name
            )
            bar()
        except Exception as e:
            logger.error(f"Error recognising audio: {e}")
            return
    
    return generated
