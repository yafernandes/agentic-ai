"""
Configuration settings for the OpenAI agents project.
"""
import os

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"

# Datadog Configuration
DD_LLMOBS_ML_APP = os.getenv("DD_LLMOBS_ML_APP")
DD_PROJECT_NAME = "HAL"
DD_DATASET_NAME = os.getenv("DD_DATASET_NAME", "Traveler")

# Cache Configuration
EMBEDDING_CACHE_SIZE = 1000

# API Configuration
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3