from .config import model_name, ollama_options, image_to_text_model_name
from .helpers import logger
from .functions.summarise_article import summarise_article
from .functions.summarise_article_split import summarise_article_split
from .functions.summarise_articles import summarise_articles
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
        if ',' in source and ' ' not in source:
            file_paths = source.split(',')
            article_texts = []
            for file_path in file_paths:
                if is_valid_filepath(file_path.strip()):
                    article_texts.append(Path(file_path.strip()).read_text(encoding="utf-8"))
                else:
                    article_texts.append(file_path.strip())
            return article_texts
        elif is_valid_filepath(source):
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
    if ',' in source and ' ' not in source:
        file_paths = source.split(',')
        names = [Path(file_path.strip()).stem for file_path in file_paths if is_valid_filepath(file_path.strip())]
        path = "_".join(names)
        return f"data/compare/{path}"
    elif is_valid_filepath(source):
        return source
    else:
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"data/article_{date_time}"

def summarise(source, should_chunk=False, compare=False):
    """
    Summarise an article using the Ollama API.

    Args:
        source (str): The name of the article to get data from or the article itself.
    
    Returns:
        str: The summary of the article.
    """
    try:
        article_text = get_data(source)
        if article_text is None:
            return

        article_name = get_data_name(source)

        if isinstance(article_text, list):
            return handle_list_articles(article_text, article_name, compare)
        elif should_chunk and compare:
            return handle_chunk_and_compare(article_text, article_name)
        elif should_chunk:
            return handle_chunk(article_text, article_name)
        else:
            return handle_single_article(article_text, article_name)
    except Exception as e:
        logger.error(f"Error summarising article: {e}")
        return


def handle_list_articles(article_text, article_name, compare):
    summaries = []
    for i, text in enumerate(article_text):
        summary = summarise_article(text, f"{article_name}_{i}", ollama_options, model_name, image_to_text_model_name)
        if summary is None:
            return ""
        summaries.append(summary)

    if compare:
        return summarise_articles(article_name, summaries, ollama_options, model_name)

    return "\n\n".join(summaries)


def handle_chunk_and_compare(article_text, article_name):
    summary_one = summarise_article(article_text, article_name, ollama_options, model_name, image_to_text_model_name)
    if summary_one is None:
        return ""
    summary_split = summarise_article_split(article_text, article_name, ollama_options, model_name)
    if summary_split is None:
        return ""
    summary_two = summarise_articles(article_name, summary_split, ollama_options, model_name)
    if summary_two is None:
        return ""

    return f"{summary_one}\n\n{summary_two}"


def handle_chunk(article_text, article_name):
    summary = summarise_article_split(article_text, article_name, ollama_options, model_name)
    if summary is None:
        return ""
    return summary


def handle_single_article(article_text, article_name):
    summary = summarise_article(article_text, article_name, ollama_options, model_name, image_to_text_model_name)
    if summary is None:
        return ""
    return summary
