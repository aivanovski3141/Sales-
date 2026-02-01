# Sales Outreach Generator

A Python CLI tool that generates personalised sales outreach messages using the Anthropic Claude API.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy the environment file and add your Anthropic API key:

```bash
cp .env.example .env
# Edit .env and replace the placeholder with your real key
```

## Usage

```bash
python generate.py examples/input.json
```

The tool reads a JSON file with the following fields:

| Field | Description |
|---|---|
| `company_name` | Name of the target company |
| `person_name` | Prospect's full name |
| `person_title` | Prospect's job title |
| `company_website_text` | Pasted text from the company website |
| `linkedin_profile_text` | Pasted text from the prospect's LinkedIn profile |

See `examples/input.json` for a complete example.

## Output

Generated messages are saved as Markdown files in the `outputs/` directory. Each file contains:

- LinkedIn outreach message
- Email outreach message
- Short follow-up message
- 15–20 second call opener

## Project Structure

```
├── generate.py          # CLI entry point
├── prompt.py            # System prompt and user prompt builder
├── examples/
│   └── input.json       # Example input file
├── outputs/             # Generated outreach messages (git-ignored)
├── requirements.txt
├── .env.example
└── CLAUDE.md
```
