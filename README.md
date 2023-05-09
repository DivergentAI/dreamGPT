# **dreamGPT**: AI powered inspiration

## Requirements

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)

## Setup

- Rename `.env.example` to `.env` and fill in the values.
  - `OPENAI_API_KEY`: Your OpenAI API key.
  - **Optional**: If you wish to store the "dreams" in Pinecone, fill in the following values:
    - `PINECONE_API_KEY`: Your Pinecone API key.
    - `PINECONE_ENVIRONMENT`: The name of the Pinecone environment.

## Run

1. Run `poetry install` to install dependencies.
2. Run `poetry run start` to start dreamGPT.
