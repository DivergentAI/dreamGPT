# **dreamGPT**: AI powered inspiration

dreamGPT, the first GPT-based solution that uses hallucinations from LLMs for divergent thinking to generate new innovative ideas. Hallucinations are often seen as a negative thing, but what if they could be used for our advantage? dreamGPT is here to show you how. The goal of dreamGPT is to explore as many possibilities as possible, as opposed to most other GPT-based solutions which are focused on solving specific problems.

<center>

<br>

![dreamGPT flow](docs/img/diamond.png)

<br>

</center>

This is how it works:

<center>

<br>

![dreamGPT flow](docs/img/dreamGPT-flow.png)

<br>

</center>

To use dreamGPT, you will need to have the following installed:

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)

## Setup

- Clonse the dreamGPT repository from GitHub:
  - `git clone https://github.com/DivergentAI/dreamGPT.git`
- Rename `.env.example` to `.env` and fill in the values.
  - `OPENAI_API_KEY`: Your OpenAI API key.
  - **Optional**: If you wish to store the "dreams" in Pinecone, fill in the following values:
    - `PINECONE_API_KEY`: Your Pinecone API key.
    - `PINECONE_ENVIRONMENT`: The name of the Pinecone environment.

Then, you can run the dreamGPT script to generate new ideas:

### Manually

1. Run `poetry install` to install dependencies.
2. Run `poetry run start` to start dreamGPT.

## Automatically

I assume that you already have docker and run it in background

1. Run `docker-compose up --build -d` to install all dependencies and start dreamGPT service
2. To stop dreamGPT service, run command `docker-compose down`

or if you prefer to use Makefile

1. Run command `make start` to install all dependencies and start dreamGPT service
2. Run command `make stop` to stop dreamGPT service

Once you run it, dreamGPT generates a random seed of concepts and will use these as a starting point for its dreaming process. Here is a screenshot of the first iteration. Notice that the scores are not very high. As dreamGPT evolves the dreams you will start to see higher scores with even better ideas.

<center>

<br>

![dreamGPT flow](docs/img/output.jpg)

<br>

</center>
