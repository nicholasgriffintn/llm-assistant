## Mixtral Research Assistant

## Introduction
The goal of this project is to develop an advanced research assistant using the Large Language Model (LLM) architecture, specifically leveraging the capabilities of the Mixtral model. This assistant is designed to help researchers by providing detailed, accurate, and contextually relevant information across a wide range of topics.

## Features

- A frontend interface for users to interact with the assistant, manage the database and view past queries and responses.
- A backend that leverages the Mixtral model and Ollama to generate responses to user queries (maybe CloudFlare in the future).
- A database to store user queries and responses for future reference.

## Technologies

- Python
- FastAPI
- Langschain
- Mixtral

## Setup

```bash
# Clone the repository
git clone https://github.com/nicholasgriffin/mixtral-assistant.git
# Navigate to the project directory
cd mixtral-assistant
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
ollama run mixtral
```

This model is around 26GB, so make sure you have enough space on your machine, also note that this download will take some time.

You can find out more about the model [here](https://ollama.com/library/mixtral).

## Testing

```bash
# Run the test suite
pytest -v
```