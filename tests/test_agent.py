import asyncio
import os
import sys
import json
from functools import lru_cache
from typing import Any

from ddtrace.llmobs import LLMObs
from ddtrace.llmobs.decorators import workflow
from sklearn.metrics.pairwise import cosine_similarity

import main_agent
from agents import Runner
from agents.run import RunConfig
from agents.model_settings import ModelSettings
from embeddings import get_embedding
from settings import DD_LLMOBS_ML_APP, DD_PROJECT_NAME, DD_DATASET_NAME


def task(input_data: str, config: dict) -> str:
    # Only create ModelSettings if temperature is provided
    if "model_temperature" in config:
        model_settings = ModelSettings(temperature=config["model_temperature"])
        runConfig = RunConfig(model=config["model_name"], model_settings=model_settings)
    else:
        runConfig = RunConfig(model=config["model_name"])

    return asyncio.run(
        Runner.run(main_agent.agent, input=input, run_config=runConfig)
    ).final_output


def semantic_similarity(
    input_data: str, output_data: str, expected_output: str
) -> float:
    emb1 = get_embedding(output_data)
    emb2 = get_embedding(expected_output)
    return cosine_similarity([emb1], [emb2])[0][0]


def test_responses():
    if not DD_LLMOBS_ML_APP:
        raise ValueError("DD_LLMOBS_ML_APP environment variable is required")

    LLMObs.enable(
        ml_app=DD_LLMOBS_ML_APP,
        project_name=DD_PROJECT_NAME,
    )

    configs = [
        {"model_name": "gpt-4.1-nano", "model_temperature": 0.1},
        {"model_name": "gpt-4.1-nano", "model_temperature": 0.5},
        {"model_name": "gpt-4.1-nano", "model_temperature": 0.9},
        {"model_name": "gpt-4o-mini", "model_temperature": 0.3},
        {"model_name": "gpt-4o-mini", "model_temperature": 0.7},
    ]

    try:
        ds = LLMObs.pull_dataset(DD_DATASET_NAME)
    except Exception as e:
        print(f"Failed to pull dataset: {e}")
        print("Uploading dataset from local JSON file...")
        with open("dataset.json", "r") as f:
            dataset_data = json.load(f)
        ds = LLMObs.create_dataset(
            name=DD_DATASET_NAME,
            description="Test data for Weather agent",
            records=dataset_data,
        )
        ds.push()

    for config in configs:
        print(f"Running for {config["model_name"]}")
        experiment = LLMObs.experiment(
            name="weather_forecast",
            description="Experiment to validate the weather forecast agent",
            dataset=ds,
            task=task,
            evaluators=[semantic_similarity],
            config=config,
        ).run(raise_errors=True)

    assert True


if __name__ == "__main__":
    test_responses()
