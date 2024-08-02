from pathlib import Path
from alive_progress import alive_bar

from ..helpers import generate_and_check, logger, generate_image_to_text, get_report_template

def analyse_article( article_text, article_name, ollama_options, model_name, image_to_text_model_name ):
    """
    Analyze a text file using the LLM.
    
    Args:
        article_text (str): The text of the article to analyze.
        article_name (str): The name of the article.
        ollama_options (dict): The options to use for generation.
        model_name (str): The model to use for generation.
    """

    logger.info(f"Analyzing article: {article_name}")

    prompt_template = get_report_template("prompts/prompt-analysis.txt")

    if not prompt_template:
        return
    
    # Get the images in the article_text
    images = []
    for line in article_text.split("\n"):
        if line.startswith("!"):
            imageURL = line.split("(")[1].split(")")[0]
            images.append(imageURL)
    
    if len(images) > 0:
        with alive_bar() as bar:
            logger.info("Images found in article. Using image-to-text model to convert images to text.")
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
            generated = generate_and_check( 
                prompt_template.format(
                    docs = article_text
                ),
                ollama_options,
                model_name,
                article_text
            )
            bar()
        except Exception as e:
            logger.error(f"Error generating analysis: {e}")
            return
    
    encoded_model_name = model_name.replace("/", "_").replace("@", "_")
    output_path = Path(f"{article_name}.analysis.{encoded_model_name}.md")
    try:
        output_path.write_text(generated, encoding="utf-8")
    except IOError as e:
        logger.error(f"Error writing analysis to file: {e}")
        return

    return generated
