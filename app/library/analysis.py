from .config import model_name, ollama_options, image_to_text_model_name
from .helpers import logger
from .functions.analyse_article import analyse_article
from  pathvalidate import is_valid_filepath
from pathlib import Path
import datetime

def get_data(source):
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

def get_data_name(source):
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
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"data/article_{date_time}"

def analysis( source ):
    """
    Analyze an article using the Ollama API.

    Args:
        source (str): The name of the article to get data from or the article itself.
    
    Returns:
        str: The analysis of the article.
    """

    try:
        article_text = get_data( source )
        if article_text is None:
            return
        
        article_name = get_data_name( source )
        
        analysis = analyse_article( article_text, article_name, ollama_options, model_name, image_to_text_model_name )

        if analysis is None:
            return ""
        
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing article: {e}")
        return
