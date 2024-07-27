from pathlib import Path
from alive_progress import alive_bar
from  pathvalidate import is_valid_filepath
import requests

from ..helpers import generate, check_summary, logger, generate_image_to_text

def summarise_article( source, ollama_options, model_name, image_to_text_model_name ):
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
    
    # Get the images in the article_text
    images = []
    for line in article_text.split("\n"):
        if line.startswith("!"):
            imageURL = line.split("(")[1].split(")")[0]
            images.append(imageURL)
    
    if len(images) > 0:
        with alive_bar() as bar:
            print("Images found in article. Using image-to-text model to convert images to text.")
            try:
                for image in images:
                    response = generate_image_to_text(image, ollama_options, image_to_text_model_name)
                    if response is not None:
                        # Replace the line that contains the image with the generated text
                        article_text = article_text.replace(f"![]({image})", f"### REPLACED_IMAGE ###\n{response}")
                bar()
            except Exception as e:
                logger.error(f"Error summarising image: {e}")

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
    
    encoded_model_name = model_name.replace("/", "_").replace("@", "_")
    output_path = Path(f"{source}.summary.{encoded_model_name}.md")
    try:
        output_path.write_text(generated, encoding="utf-8")
    except IOError as e:
        logger.error(f"Error writing summary to file: {e}")
        return

    summary_check = check_summary(generated, article_text)
    logger.info(f"Overall summary passes check? {summary_check}")

    return generated
