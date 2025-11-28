"""Utility script to test the LLM-based transcript rewrite in isolation."""

import os
import sys
import click
from dotenv import load_dotenv
from openai import OpenAI


SYSTEM_PROMPT = "You are a helpful assistant who follows the user's formatting instructions carefully."


def rewrite_transcript(transcript: str, model: str = "gpt-4o-mini") -> str:
    """Rewrite transcript with the same rules as generations_v2."""
    client = OpenAI()
    user_prompt = (
        "Rewrite the transcript for TTS.\n"
        "- Convert digits to words (e.g., 42 -> forty-two, 2024 -> two thousand twenty-four).\n"
        "- Remove special characters like quotes, parentheses, square brackets, and curly braces unless they are part "
        "of tags such as [SPEAKER0]. Keep those tags intact.\n"
        "- Expand compressed forms when obvious: US -> United States, UK -> United Kingdom, C -> degrees Celsius, "
        "HCMC -> Ho Chi Minh City.\n"
        "- Return only the cleaned transcript, nothing else.\n\n"
        f"Transcript:\n{transcript}"
    )
    completion = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return completion.choices[0].message.content.strip()


# @click.command()
# @click.option(
#     "--transcript_path",
#     type=click.Path(exists=True, dir_okay=False),
#     help="Path to a transcript file. If omitted, reads from stdin.",
# )
# @click.option(
#     "--model",
#     default="gpt-4o-mini",
#     help="OpenAI model to use for rewriting.",
# )
def main(transcript_path: str, model: str):
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"), override=False)
    if not os.getenv("OPENAI_API_KEY"):
        click.echo("OPENAI_API_KEY not set. Set it in .env or your environment.", err=True)
        sys.exit(1)

    if transcript_path:
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = f.read()
    else:
        transcript = sys.stdin.read()

    transcript = transcript.strip()
    if not transcript:
        click.echo("No transcript provided.", err=True)
        sys.exit(1)

    rewritten = rewrite_transcript(transcript, model=model)
    click.echo(rewritten)

transcript_path: str = "/home/kriz-wu/Workload/Projects/intern/higgs-audio/examples/transcript/single_speaker/custom_podcast_1_raw.txt"
model: str = "gpt-4o-mini"


if __name__ == "__main__":
    main(transcript_path=transcript_path, model=model)
