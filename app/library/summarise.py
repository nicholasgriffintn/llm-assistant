from .config import model_name, ollama_options, image_to_text_model_name
from .helpers import logger
from .functions.summarise_article import summarise_article
from .functions.summarise_article_split import summarise_article_split
from .functions.summarise_articles import summarise_articles
from  pathvalidate import is_valid_filepath
from pathlib import Path
import datetime

def get_data( source ):
    """
    Get the data from the source, either a file or text.

    Args:
        source (str): The name of the article to get data from or the article itself.
    
    Returns:
        str: The article text.
    """

    try:
        if is_valid_filepath(source):
            article_text = Path(source).read_text(encoding="utf-8")
        else:
            article_text = source
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return
    except IOError as e:
        logger.error(f"Error reading file: {e}")
        return
    
    return article_text

def get_data_name( source ):
    """
    Generate a name for the data source.

    Args:
        source (str): The name of the article to get data from or the article itself.

    Returns:
        str: The name of the data source.
    """

    if is_valid_filepath(source):
        return source
    else:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"data/article_{date_time}"

def summarise( source, should_chunk=False, compare=False ):
    """
    Summarise an article using the Ollama API.

    Args:
        source (str): The name of the article to get data from or the article itself.
    
    Returns:
        str: The summary of the article.
    """

    try:
        article_text = get_data( source )
        if article_text is None:
            return
        
        article_name = get_data_name( source )

        if should_chunk and compare:
            summary_one = summarise_article( article_text, article_name, ollama_options, model_name, image_to_text_model_name )
            if summary_one is None:
                return ""
            summary_split = summarise_article_split( article_text, article_name, ollama_options, model_name )
            if summary_split is None:
                return ""
            summary_two = summarise_articles( article_name, summary_split, ollama_options, model_name )
            if summary_two is None:
                return ""

            summary = f"{summary_one}\n\n{summary_two}"
        elif should_chunk:
            summary = summarise_article_split( article_text, article_name, ollama_options, model_name )
        else:
            summary = summarise_article( article_text, article_name, ollama_options, model_name, image_to_text_model_name )

        if summary is None:
            return ""
        
        return summary
    except Exception as e:
        logger.error(f"Error summarising article: {e}")
        return
