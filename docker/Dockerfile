# Start with the official Python 3.10 image
FROM python:3.10

# Install poetry
RUN pip install poetry

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in pyproject.toml
RUN poetry install

# Run the application command
CMD ["poetry", "run", "start"]
