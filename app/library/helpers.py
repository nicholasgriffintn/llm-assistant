import os.path
import markdown
import requests
import logging
import re
import string

from .config import ollama_host, use_cloudflare, cloudflare_api_token, cloudflare_host, cloudflare_account_id

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

def generate(prompt, options, model_name):
    """
    Generate text using the Ollama API.

    Args:
        prompt (str): The prompt to generate text from.
        options (dict): The options to use for generation.
        model_name (str): The model to use for generation.

    Returns:
        str: The generated text.
    """

    if use_cloudflare:
        if cloudflare_api_token is None or cloudflare_host is None or cloudflare_account_id is None:
            logger.error("Cloudflare API key, host, or account ID not set.")
            return None
        
        url = f"{cloudflare_host}/client/v4/accounts/{cloudflare_account_id}/ai/run/{model_name}"
        headers = {
            "Authorization": f"Bearer {cloudflare_api_token}",
        }
        inputs = [
            { "role": "user", "content": prompt }
        ];
        payload = {
            "messages": inputs
        }
    else:
        url = f"{ollama_host}/api/generate"
        headers = {}
        payload = {
            "prompt": prompt,
            "model": model_name,
            "stream": False,
            "options": options
        }
    
    try:
        print(f"Requesting generation from {url}...")
        response = requests.post(url, headers=headers, json=payload, timeout=180)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print(f"Response: {response.json()}")
        if use_cloudflare:
            responseJson = response.json()
            result = responseJson.get("result")
            if result is None:
                logger.error("No response from server")
                return None
            success = responseJson.get("success")
            if success is not True:
                logger.error("Request failed")
                return None
            return result.get("response")
        else:
            return response.json().get("response")
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    return None

def generate_image_to_text(image, ollama_options, image_to_text_model_name):
    res = requests.get(image)
    blob = res.content
    input_data = {
        "image": list(blob),
        "prompt": "Generate a caption for this image",
        "max_tokens": 512,
    }
    if use_cloudflare:
        url = f"{cloudflare_host}/client/v4/accounts/{cloudflare_account_id}/ai/run/{image_to_text_model_name}"
        headers = {
            "Authorization": f"Bearer {cloudflare_api_token}",
        }
        response = requests.post(url, headers=headers, json=input_data, timeout=180)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        responseJson = response.json()
        result = responseJson.get("result")
        if result is None:
            logger.error("No response from server")
            return None
        success = responseJson.get("success")
        if success is not True:
            logger.error("Request failed")
            return None
        return result.get("description")
    else:
        url = f"{ollama_host}/api/generate"
        headers = {}
        payload = {
            "prompt": input_data["prompt"],
            "model": image_to_text_model_name,
            "stream": False,
            "options": ollama_options,
            "inputs": input_data
        }
        response = requests.post(url, headers=headers, json=payload, timeout=180)
        response.raise_for_status()

        return response.json().get("response")

def check_summary(summary, article):
    """
    Check if the summary quotes are sufficiently represented in the article.

    Args:
        summary (str): The summary containing quotes.
        article (str): The article to check against.

    Returns:
        bool: True if all quotes in the summary are sufficiently represented in the article, False otherwise.
    """
    
    # Find quotes in the summary
    matches = re.findall(r'"(.*?)"', summary)
    article = article.lower()

    for match in matches:
        match = match.lower()
        parts = match.split("...")
        for part in parts:
            words = part.split()
            valid_words = sum(1 for word in words if word.strip(string.punctuation) in article)
            if len(words) == 0:
                return True
            pc_valid = valid_words / len(words)
            logger.info(f"pc_valid: {pc_valid}")
            if pc_valid < 0.8:
                return False
    return True
