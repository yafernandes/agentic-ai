import asyncio
import os
import sys
import json
from functools import lru_cache
from typing import Any

import ddtrace.llmobs.experimentation as dne
from sklearn.metrics.pairwise import cosine_similarity

import main_agent
from agents import Runner
from agents.run import RunConfig
from agents.model_settings import ModelSettings
from embeddings import get_embedding
from settings import DD_LLMOBS_ML_APP, DD_PROJECT_NAME, DD_DATASET_NAME


@dne.task
def ask(input: str, config: dict) -> str:
    # Only create ModelSettings if temperature is provided
    if "model_temperature" in config:
        model_settings = ModelSettings(temperature=config["model_temperature"])
        runConfig = RunConfig(model=config["model_name"], model_settings=model_settings)
    else:
        runConfig = RunConfig(model=config["model_name"])

    return asyncio.run(
        Runner.run(main_agent.agent, input=input, run_config=runConfig)
    ).final_output


@dne.evaluator
def semantic_similarity(input: str, output: str, expected_output: str) -> float:
    emb1 = get_embedding(output)
    emb2 = get_embedding(expected_output)
    return cosine_similarity([emb1], [emb2])[0][0]


def test_responses():
    if not DD_LLMOBS_ML_APP:
        raise ValueError("DD_LLMOBS_ML_APP environment variable is required")

    dne.init(
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
        ds = dne.Dataset.pull(DD_DATASET_NAME)
    except Exception as e:
        print(f"Failed to pull dataset: {e}")
        print("Uploading dataset from local JSON file...")
        with open("dataset.json", "r") as f:
            dataset_data = json.load(f)
        ds = dne.Dataset(name=DD_DATASET_NAME, data=dataset_data)
        ds.push(new_version=True)

    for config in configs:
        print(f"Running for {config["model_name"]}")
        experiment = dne.Experiment(
            name="weather_forecast",
            description="Experiment to validate the weather forecast agent",
            dataset=ds,
            task=ask,
            evaluators=[semantic_similarity],
            config=config,
        ).run(raise_errors=True)

    assert True


if __name__ == "__main__":
    test_responses()
