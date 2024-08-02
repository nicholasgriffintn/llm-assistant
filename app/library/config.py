import os

model_name = os.getenv("MODEL_NAME", "mistral-nemo")
image_to_text_model_name = os.getenv("IMAGE_TO_TEXT_MODEL_NAME", "llava")
text_to_image_model_name = os.getenv("TEXT_TO_IMAGE_MODEL_NAME", "mistral-nemo")
speech_recognition_model_name = os.getenv("SPEECH_RECOGNITION_MODEL_NAME", "mistral-nemo")

ollama_options = {
    "seed": 42,
    "temperature": 0.0,
    "top_k" : 10,
    "top_p" : 0.5,
}

ollama_host = "http://localhost:11434"

use_cloudflare = os.getenv("USE_CLOUDFLARE", "false") == "true"

cloudflare_api_token = os.getenv("CLOUDFLARE_API_TOKEN")
cloudflare_host = "https://api.cloudflare.com"
cloudflare_account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
cloudflare_ai_endpoint = f"client/v4/accounts/{cloudflare_account_id}/ai/run"
cloudflare_gateway_host = "https://gateway.ai.cloudflare.com"
cloudflare_gateway_id = os.getenv("CLOUDFLARE_GATEWAY_ID")
if cloudflare_gateway_id is not None:
    cloudflare_host = cloudflare_gateway_host
    cloudflare_ai_endpoint = f"v1/{cloudflare_account_id}/{cloudflare_gateway_id}/workers-ai"
