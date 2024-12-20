from .config import model_name, ollama_options, image_to_text_model_name
from .helpers import logger
from .functions.answer_question import answer_question

def question( source, should_stream=False ):
    """
    Answer a question using the Ollama API.

    Args:
        source (str): The contents of the question.
        should_stream (bool): Whether to stream the response.
    
    Returns:
        str: The answer to the question.
    """

    try:
        question = source
        if question is None:
            return
        
        analysis = answer_question( question, ollama_options, model_name, should_stream )

        if analysis is None:
            return ""
        
        return analysis
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return
