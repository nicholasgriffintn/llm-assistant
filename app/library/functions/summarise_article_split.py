from langchain.text_splitter import RecursiveCharacterTextSplitter
import random
from alive_progress import alive_it
from pathlib import Path

from ..helpers import generate, check_summary, logger

def summarise_article_split(source, article_text, prompt_template, ollama_options, model_name):
    """
    Summarise an article by splitting it into smaller chunks and recursively summarising those chunks.

    Args:
        source (str): The name of the article.
        article_text (str): The text of the article.
        prompt_template (str): The template for the prompt.
        ollama_options (dict): Options for the ollama model.
        model_name (str): The name of the model to use.
    """
    chunk_size = len(article_text) // 7  # or a fixed size, like 4096 or something
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    splits = text_splitter.split_text(article_text)

    logger.info(f"Split text into {len(splits)} chunks...")

    summaries = []
    attempts = 0

    for i, split in enumerate(alive_it(splits)):
        summary_ok = False
        retries = 5
        options = ollama_options.copy()

        while not summary_ok and retries > 0:
            attempts += 1
            try:
                summary = generate(
                    prompt_template.format(docs=split),
                    options,
                    model_name
                )
                summary_ok = check_summary(summary, article_text)
                if summary_ok:
                    summaries.append(summary)
                    logger.info(f"Chunk #{i} summary generated successfully.")
                    encoded_model_name = model_name.replace("/", "_").replace("@", "_")
                    Path(f"{source}.summary.{encoded_model_name}.{i}.md").write_text(summary, encoding="utf-8")
                else:
                    logger.warning(f"Chunk #{i} summary failed. Retries left: {retries - 1}...")
                    retries -= 1
                    options["seed"] = random.randint(0, 10000)
                    options["temperature"] += 0.1
            except Exception as e:
                logger.error(f"Error generating summary for chunk #{i}: {e}")
                retries -= 1

        if not summary_ok:
            logger.error(f"Failed to generate summary for chunk #{i} after multiple attempts.")
            return

    logger.info(f"Finished. Generated summaries for {len(splits)} chunks in {attempts} total attempts.")

    return summaries
