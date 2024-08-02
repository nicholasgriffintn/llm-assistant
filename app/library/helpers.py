import os.path
import markdown
import requests
import logging
import re
import string
import random
from pathlib import Path
import base64

from .config import ollama_host, use_cloudflare, cloudflare_api_token, cloudflare_host, cloudflare_account_id, cloudflare_ai_endpoint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def openfile(filename):
    """
    Open a file and return its contents as HTML.

    Args:
        filename (str): The name of the file to open.

    Returns:
        dict: The contents of the file as HTML, or an error message.
    """

    filepath = os.path.join("app/pages/", filename)
    
    try:
        with open(filepath, "r", encoding="utf-8") as input_file:
            text = input_file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return {"error": "File not found"}
    except IOError as e:
        logger.error(f"Error reading file {filepath}: {e}")
        return {"error": "Error reading file"}

    html = markdown.markdown(text)
    return {"text": html}

def get_report_template(path):
    """
    Get the report template.

    Returns:
        str: The contents of the report template.
    """

    report_template_path = Path(path)
    try:
        report_template = report_template_path.read_text(encoding="utf-8")
        return report_template
    except FileNotFoundError:
        logger.error(f"Template file not found: {report_template_path}")
        return
    except IOError as e:
        logger.error(f"Error reading template file: {e}")
        return
    
def post_generate_request(url, headers, payload, should_stream, response_type="json"):
    """
    Make a POST request to the LLM API.

    Args:
        url (str): The URL to make the request to.
        headers (dict): The headers to include in the request.
        payload (dict): The payload to include in the request.
        should_stream (bool): Whether to stream the response.
    
    Returns:
        dict: The response from the server.
    """

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=180)
        response.raise_for_status()

        if should_stream:
            inference = response
            return inference
        else:
            if response_type == "json":
                inference = response.json()
            if response_type == "binary":
                inference = response.content
            else:
                inference = response.text
            return inference
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

def generate(prompt, options, model_name, should_stream=False):
    """
    Generate text using the Ollama API.

    Args:
        prompt (str): The prompt to generate text from.
        options (dict): The options to use for generation.
        model_name (str): The model to use for generation.
        should_stream (bool): Whether to stream the response.

    Returns:
        str: The generated text.
    """

    if use_cloudflare:
        if not all([cloudflare_api_token, cloudflare_host, cloudflare_account_id, cloudflare_ai_endpoint]):
            logger.error("Cloudflare API key, host, or account ID not set.")
            return None
        
        url = f"{cloudflare_host}/{cloudflare_ai_endpoint}/{model_name}"
        headers = {
            "Authorization": f"Bearer {cloudflare_api_token}",
        }
        payload = {
            "prompt": prompt,
            "stream": should_stream,
            "seed": options.get("seed"),
            "temperature": options.get("temperature"),
            "top_k": options.get("top_k"),
            "top_p": options.get("top_p"),
        }
    else:
        url = f"{ollama_host}/api/generate"
        headers = {}
        payload = {
            "prompt": prompt,
            "model": model_name,
            "stream": should_stream,
            "options": options
        }
    
    response_json = post_generate_request(url, headers, payload, should_stream)
    if not response_json:
        return None
    
    if should_stream:
        return response_json

    if use_cloudflare:
        result = response_json.get("result")
        if result is None or not response_json.get("success"):
            logger.error("Request failed or no response from server")
            return None
        return result.get("response")
    else:
        return response_json.get("response")
    
def generate_and_check(prompt, ollama_options, model_name, article_text):
    """
    Generate text and check if it is sufficiently represented in the article.

    Args:
        prompt (str): The prompt to generate text from.
        options (dict): The options to use for generation.
        model_name (str): The model to use for generation.
        article_text (str): The article to check against.

    Returns:
        str: The generated text if it is sufficiently represented in the article, None otherwise.
    """

    generation_matches = False
    generation = None
    options = ollama_options.copy()
    num_retries = 2
    attempts = 0

    while not generation_matches and num_retries > 0:
        attempts += 1

        logger.info(f"Attempt #{attempts} to generate text...")

        try:
            generation = generate(prompt, ollama_options, model_name)
            generation_matches = check_summary(generation, article_text)

            if generation_matches:
                logger.info("Generation successful.")
            else:
                logger.info("Generation failed. Adjusting options and retrying...")
                num_retries -= 1

                options["seed"] = random.randint(0, 10000)
                options["temperature"] += 0.1
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            num_retries -= 1
    
    if not generation_matches:
        logger.error(f"Failed to generate text after {attempts} attempts.")
        return None
    
    return generation

def generate_image_to_text(image, ollama_options, image_to_text_model_name):
    res = requests.get(image)
    blob = res.content

    payload = {
        "prompt": "Generate a caption for this image",
        "stream": False,
    }

    if use_cloudflare:
        url = f"{cloudflare_host}/client/v4/accounts/{cloudflare_account_id}/ai/run/{image_to_text_model_name}"
        headers = {
            "Authorization": f"Bearer {cloudflare_api_token}",
        }
        payload.update({
            "image": list(blob),
            "max_tokens": 512,
            "seed": ollama_options.get("seed"),
            "temperature": ollama_options.get("temperature"),
            "top_k": ollama_options.get("top_k"),
            "top_p": ollama_options.get("top_p"),
        })
    else:
        url = f"{ollama_host}/api/generate"
        headers = {}
        payload.update({
            "images": [blob],
            "model": image_to_text_model_name,
            "options": ollama_options,
        })

    response_json = post_generate_request(url, headers, payload)
    if not response_json:
        return None

    if use_cloudflare:
        result = response_json.get("result")
        if result is None or not response_json.get("success"):
            logger.error("Request failed or no response from server")
            return None
        return result.get("description")
    else:
        return response_json.get("response")
    
def generate_text_to_image(prompt, options, text_to_image_model_name):
    if use_cloudflare:
        if not all([cloudflare_api_token, cloudflare_host, cloudflare_account_id, cloudflare_ai_endpoint]):
            logger.error("Cloudflare API key, host, or account ID not set.")
            return None
        
        url = f"{cloudflare_host}/{cloudflare_ai_endpoint}/{text_to_image_model_name}"
        headers = {
            "Authorization": f"Bearer {cloudflare_api_token}",
        }
        payload = {
            "prompt": prompt,
            "stream": False,
            "seed": options.get("seed"),
            "temperature": options.get("temperature"),
            "top_k": options.get("top_k"),
            "top_p": options.get("top_p"),
        }
    else:
        url = f"{ollama_host}/api/generate"
        headers = {}
        payload = {
            "prompt": prompt,
            "model": text_to_image_model_name,
            "stream": False,
            "options": options
        }

    binary_data = post_generate_request(url, headers, payload, should_stream=False, response_type="binary")
    if not binary_data:
        return None
    
    if isinstance(binary_data, str):
        binary_data = binary_data.encode('utf-8')

    base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')
    return base64_encoded_data

def check_summary(summary, article):
    """
    Check if the summary quotes are sufficiently represented in the article.

    Args:
        summary (str): The summary containing quotes.
        article (str): The article to check against.

    Returns:
        bool: True if all quotes in the summary are sufficiently represented in the article. False otherwise (including if there are no quotes).
    """

    if not summary or not article:
        logger.warning("Empty summary or article provided.")
        return False

    # Find quotes in the summary
    matches = re.findall(r'"(.*?)"', summary)
    if not matches:
        logger.info("No quotes found in the summary.")
        return False

    article = article.lower()

    for match in matches:
        match = match.lower()
        parts = match.split("...")
        for part in parts:
            words = part.split()
            if len(words) == 0:
                return True
            valid_words = sum(1 for word in words if word.strip(string.punctuation) in article)
            pc_valid = valid_words / len(words)
            logger.info(f"Quote: '{part}', Valid words: {valid_words}/{len(words)}, pc_valid: {pc_valid:.2f}")
            if pc_valid < 0.8:
                return False
    return True
