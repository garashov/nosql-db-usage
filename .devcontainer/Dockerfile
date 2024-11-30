# Use an official Python image with Python 3.11.9
FROM python:3.11.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean

# Set the working directory
WORKDIR /workspace

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the default user
ARG USERNAME=vscode
RUN useradd -ms /bin/bash $USERNAME
USER $USERNAME
