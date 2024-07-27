from pathlib import Path
from alive_progress import alive_bar
from  pathvalidate import is_valid_filepath

from ..helpers import generate, check_summary, logger

def summarise_article( source, ollama_options, model_name ):
    """
    Summarise a text file using the LLM.
    
    Args:
        source (str): The name of the file to summarise.
        ollama_options (dict): The options to use for generation.
        model_name (str): The model to use for generation.
    """

    try:
        if is_valid_filepath(source):
            article_text = Path(source).read_text(encoding="utf-8")
        else:
            article_text = source
        prompt_template = Path("prompts/prompt-summary.txt").read_text(encoding="utf-8")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return
    except IOError as e:
        logger.error(f"Error reading file: {e}")
        return

    generated = None
    with alive_bar() as bar:
        try:
            generated = generate( 
                prompt_template.format(
                    docs = article_text
                ),
                ollama_options,
                model_name
            )
            bar()
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return
    
    output_path = Path(f"app/pages/{source}.summary.{model_name}.md")
    try:
        output_path.write_text(generated, encoding="utf-8")
    except IOError as e:
        logger.error(f"Error writing summary to file: {e}")
        return

    summary_check = check_summary(generated, article_text)
    logger.info(f"Overall summary passes check? {summary_check}")
    print(f"Overall summary passes check? {summary_check}")

    return generated
