import os

model_name = os.getenv("MODEL_NAME", "mistral-nemo")

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