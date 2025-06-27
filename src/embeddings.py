import os
from functools import lru_cache

import openai

from settings import OPENAI_API_KEY, EMBEDDING_MODEL, EMBEDDING_CACHE_SIZE

client = openai.OpenAI(api_key=OPENAI_API_KEY)


@lru_cache(maxsize=EMBEDDING_CACHE_SIZE)
def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding