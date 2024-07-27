from .config import model_name, ollama_options, image_to_text_model_name
from .helpers import logger
from .functions.summarise_article import summarise_article
from .functions.summarise_article_split import summarise_article_split
from .functions.summarise_articles import summarise_articles

def summarise( source ):
    """
    Summarise an article using the Ollama API.

    Args:
        source (str): The name of the article to summarise.
    
    Returns:
        str: The summary of the article.
    """

    try:
        summary = summarise_article( source, ollama_options, model_name, image_to_text_model_name )

        if summary is None:
            return ""
        
        return summary
    except Exception as e:
        logger.error(f"Error summarising article: {e}")
        return
