## LLaMA Research Assistant

## Introduction
The goal of this project is to develop an advanced research assistant using the Large Language Model (LLM) architecture, specifically leveraging the capabilities of the LLaMA (Large Language Model Meta AI) model. This assistant is designed to help researchers by providing detailed, accurate, and contextually relevant information across a wide range of topics.

## Features

- A frontend interface for users to interact with the assistant, manage the database and view past queries and responses.
- A backend that leverages the LLaMA model to generate responses to user queries.
- A database to store user queries and responses for future reference.

## Technologies

- Python
- FastAPI
- Langsmith
- Langschain
- NumPy

## Setup

```bash
# Clone the repository
git clone https://github.com/nicholasgriffin/llama-assistant.git
# Navigate to the project directory
cd llama-assistant
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

## Testing

```bash
# Run the test suite
pytest -v
```