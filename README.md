# Agentic AI - Weather Forecasting Agents

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)

An OpenAI agents-based application that provides weather forecasting using intelligent agents. The system includes a weather agent with tools for geocoding, weather data retrieval, and date calculations.

## Project Structure

```text
src/
├── main.py              # Main agent entry point
├── weather_agent.py     # Weather forecasting agent
├── weather_tools.py     # Weather-related tools and functions
├── settings.py          # Configuration settings
└── embeddings.py        # Embedding utilities
tests/                   # Experiments and unit tests
scripts/                 # Demo and utility scripts
```

## Setup

### 1. Install the package

```bash
pip install -e .
```

### 2. Environment Variables

Ensure these environment variables are set:

```bash
export OPENAI_API_KEY=your_openai_api_key
export DD_API_KEY=your_datadog_api_key
export DD_APPLICATION_KEY=your_datadog_app_key
export DD_SITE=datadoghq.com
export DD_LLMOBS_ENABLED=1
export DD_LLMOBS_ML_APP=your_ml_app_name
export DD_DATASET_NAME=your_dataset_name  # Optional, defaults to "Traveler"
```

## Usage

### Interactive Demo

```bash
python scripts/run_agentic_app.py
```

### Run Experiments

```bash
python tests/test_agent.py
```
