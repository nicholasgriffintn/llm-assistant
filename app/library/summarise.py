from .config import model_name, ollama_options
from .helpers import logger
from .functions.summarise_article import summarise_article

def summarise( article_name ):
    """
    Summarise an article using the Ollama API.

    Args:
        article_name (str): The name of the article to summarise.
    
    Returns:
        str: The summary of the article.
    """

    try:
        summary = summarise_article( article_name, ollama_options, model_name )

        print(summary)

        if summary is None:
            return "Error summarising article"

        return summary
    except Exception as e:
        logger.error(f"Error summarising article: {e}")
        return
