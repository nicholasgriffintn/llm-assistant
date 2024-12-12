## LLM Assistant

> Update: This funcationality has now moved to my new assistant project which is running in TypeScript and includes a range of features, not just article analysis and questions. https://github.com/nicholasgriffintn/assistant

## Introduction
The goal of this project is to develop an advanced assistant using the Large Language Model (LLM) architecture, specifically leveraging the capabilities of the Mistral model.

## Features

- A frontend interface for users to interact with the assistant, manage the database and view past queries and responses.
- A backend that leverages the Mixtral model and Ollama/ Cloudflare AI to generate responses to user queries.
- [ ] A database to store user queries and responses for future reference. (maybe in the future).

## Technologies

- Python
- FastAPI
- Langchain
- Mistral (mistral-nemo and mistral-7b-instruct)
- LLava
- Ollama
- Cloudflare

## Setup

```bash
# Clone the repository
git clone https://github.com/nicholasgriffin/llm-assistant.git
# Navigate to the project directory
cd llm-assistant
# Create a virtual environment
python3 -m venv venv
# Activate the virtual environment
source venv/bin/activate
# Install the required dependencies
pip install -r requirements.txt
# Run the FastAPI server
uvicorn app.main:app --reload --port 8080
```

The app will be accessible at `http://localhost:8080`.

## Setting up Ollama

If you haven't already, you will need to download and set up Ollama. You can find the instructions [here](https://github.com/ollama/ollama/blob/main/README.md#quickstart).

After that, you will need to run the Mixtral model using the following command:

```bash
ollama pull mistral-nemo
```

This model is around 7GB, so make sure you have enough space on your machine, also note that this download will take some time.

You can find out more about the model [here](https://ollama.com/library/mixtral-nemo).

You can change the model being used by setting the `MODEL_NAME` environment variable.

## Image to Text Generation

If an image (or multiple) is found in the provided query, the assistant will attempt to describe that image, this is configured to use the `llava` model by default, but you can change this by setting the `IMAGE_MODEL_NAME` environment variable.

You'll need to also pull the `llava` model using the following command in order for this to work:

```bash
ollama pull llava
```

You can find out more about the model [here](https://ollama.com/library/llava).

## Using Cloudflare

If you'd like to use Cloudflare's AI service to generate responses instead, you can set the `USE_CLOUDFLARE` environment variable to `true`.

You'll also need to set the `CLOUDFLARE_API_TOKEN` environment variable to your Cloudflare API token and the `CLOUDFLARE_ACCOUNT_ID` environment variable to your Cloudflare account ID.

You can find out more about Cloudflare's AI service [here](https://developers.cloudflare.com/ai/).

### Cloudflare Models

On Cloudflare, I have been using `@cf/mistral/mistral-7b-instruct-v0.1` as a replacement for the `mistral-nemo` model and `@cf/llava-hf/llava-1.5-7b-hf` as a replacement for the `llava` model.

### Cloudflare AI Gateway

The Cloudflare AI Gateway is pretty cool, it allows you to track usage of CloudFlare AI, set rate limits for requests and, possibly the coolest thing, cache responses for a certain amount of time.

You can find out more about the Cloudflare AI Gateway [here](https://developers.cloudflare.com/ai-gateway/).

To use it, set the env variable `CLOUDFLARE_GATEWAY_ID` to the ID of your Cloudflare AI Gateway.

## Prompt Engineering

The AI functions use a number of prompts to generate responses. These prompts are stored in the `prompts` folder as text files. You can add, remove or edit these prompts to change the behavior of the AI.

If you'd like to learn more about prompt engineering, you can read [this documentation](https://www.promptingguide.ai/models/mixtral) which talks about how to format prompts for mixtral (which we are using) and other models.

## Testing

```bash
# Run the test suite
pytest -v
```
