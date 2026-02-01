#!/usr/bin/env python3
"""Sales outreach generator — CLI tool that reads a JSON input file and
produces personalised outreach messages via the Anthropic Claude API."""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from prompt import SYSTEM_PROMPT, build_user_prompt

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent / "outputs"
REQUIRED_FIELDS = [
    "company_name",
    "person_name",
    "person_title",
    "company_website_text",
    "linkedin_profile_text",
]


def load_input(path: str) -> dict:
    logger.info("Reading input file: %s", path)
    with open(path) as f:
        data = json.load(f)
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"Input JSON is missing required fields: {missing}")
    return data


def call_claude(user_prompt: str) -> str:
    client = anthropic.Anthropic()
    logger.info("Calling Claude API …")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text


def save_output(text: str, company_name: str, person_name: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    slug = f"{company_name}_{person_name}".replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{slug}_{timestamp}.md"
    path = OUTPUT_DIR / filename
    path.write_text(text)
    logger.info("Output saved to %s", path)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate sales outreach messages from a JSON input file."
    )
    parser.add_argument("input_file", help="Path to JSON input file")
    args = parser.parse_args()

    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.")
        sys.exit(1)

    data = load_input(args.input_file)
    user_prompt = build_user_prompt(
        company_name=data["company_name"],
        person_name=data["person_name"],
        person_title=data["person_title"],
        company_website_text=data["company_website_text"],
        linkedin_profile_text=data["linkedin_profile_text"],
    )
    result = call_claude(user_prompt)
    output_path = save_output(result, data["company_name"], data["person_name"])
    print(f"\nDone. Output written to {output_path}\n")


if __name__ == "__main__":
    main()
