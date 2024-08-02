from pathlib import Path
from alive_progress import alive_bar

from ..helpers import generate, logger, get_report_template

def answer_question( question, ollama_options, model_name, should_stream=False ):
    """
    Answer a question using the LLM.
    
    Args:
        question (str): The question to answer.
        ollama_options (dict): The options to use for generation.
        model_name (str): The model to use for generation.
        should_stream (bool): Whether to stream the response.
    """

    logger.info(f"Answering question: {question}")

    prompt_template = get_report_template("prompts/prompt-question.txt")

    if not prompt_template:
        return
    
    generated = None
    with alive_bar() as bar:
        try:
            generated = generate( 
                prompt_template.format(
                    question = question
                ),
                ollama_options,
                model_name,
                should_stream
            )
            bar()
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return
    
    return generated
