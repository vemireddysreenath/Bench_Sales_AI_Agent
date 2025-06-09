# Bench Sales AI Agent

This project implements a local job application agent that can search and apply for jobs on multiple portals. It uses Playwright for browser automation and a local LLM (e.g. Ollama with Llama3) for text analysis.

## Features

 - Reads resume text from a PDF or Word (.docx) file.
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

2. Update `data/config.yaml` with search keywords, locations, resume path, LLM URL and your LinkedIn credentials.
   You can store credentials directly in the file or reference environment variables.
3. Place your resume file (PDF or DOCX) in the path specified by `resume_path`.
4. Run the agent:

```bash
python main.py
```

The agent will search LinkedIn for matching jobs and try to apply automatically.

## Configuration

`data/config.yaml` contains the following keys:

- `keywords`: list of job search keywords.
- `locations`: list of desired job locations.
- `portals`: enabled job portals (e.g. `linkedin`).
- `resume_path`: path to your PDF or DOCX resume file.
- `llm_url`: local LLM endpoint used for text analysis.
- `linkedin_username` / `linkedin_password`: credentials for LinkedIn login.

Credentials can also be supplied via environment variables referenced from the file.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

