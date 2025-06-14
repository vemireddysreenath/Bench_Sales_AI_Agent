# Bench Sales AI Agent

This project implements a local job application agent that can search and apply for jobs on multiple portals. It uses Playwright for browser automation and a local LLM (e.g. Ollama with Llama3) for text analysis.

## Features


- Uses a local LLM to evaluate job fit and to tailor the resume summary for each job.
- Plugin based architecture so new job portals can be added easily.
- Maintains an application history in SQLite to avoid duplicates.
- Logs each application attempt to a CSV file.
- Records questions for ambiguous form fields to a YAML file for manual review.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```


4. Run the agent:

```bash
python main.py
```

The agent will search LinkedIn for matching jobs and try to apply automatically.

