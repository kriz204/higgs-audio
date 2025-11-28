#!/usr/bin/env bash
set -euo pipefail

# Use the project virtualenv Python by default; override with PYTHON if needed.
PYTHON="${PYTHON:-./higgs_audio_env/bin/python}"

"${PYTHON}" examples/generations_v2.py \
  --transcript examples/transcript/single_speaker/custom_podcast_1_raw.txt \
  --scene_prompt examples/scene_prompts/quiet_indoor.txt \
  --user_text examples/voice_prompts/en_man.txt \
  --user_voice examples/voice_prompts/en_man.wav \
  --out_path test/test_en_man.wav \
  --max_new_tokens 10000 \
  --chunk_method word \
  --rewrite_transcript 
