from langchain.text_splitter import RecursiveCharacterTextSplitter
import random
from alive_progress import alive_it
from pathlib import Path

from ..helpers import generate_and_check, logger

def summarise_article_split(article_text, article_name, ollama_options, model_name):
    """
    Summarise an article by splitting it into smaller chunks and recursively summarising those chunks.

    Args:
        article_text (str): The text of the article.
        article_name (str): The name of the article.
        ollama_options (dict): Options for the ollama model.
        model_name (str): The name of the model to use.
    """

    logger.info(f"Summarising article by splitting: {article_name}")

    prompt_template_path = Path("prompts/prompt-summary.txt")
    try:
        prompt_template = prompt_template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.error(f"Template file not found: {prompt_template_path}")
        return
    except IOError as e:
        logger.error(f"Error reading template file: {e}")
        return
    
    chunk_size = len(article_text) // 7  # or a fixed size, like 4096 or something
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    splits = text_splitter.split_text(article_text)

    logger.info(f"Split text into {len(splits)} chunks...")

    summaries = []

    for i, split in enumerate(alive_it(splits)):
        try:
            summary = generate_and_check(
                prompt_template.format(docs=split),
                ollama_options,
                model_name,
                article_text
            )
            if summary:
                summaries.append(summary)
                logger.info(f"Chunk #{i} summary generated successfully.")
                encoded_model_name = model_name.replace("/", "_").replace("@", "_")
                Path(f"{article_name}.summary.{encoded_model_name}.chunk_{i}.md").write_text(summary, encoding="utf-8")
            else:
                logger.error(f"Failed to generate summary for chunk #{i} after multiple attempts.")

        except Exception as e:
            logger.error(f"Error generating summary for chunk #{i}: {e}")

    logger.info(f"Finished. Generated summaries for {len(splits)} chunks.")

    return summaries
