#!/usr/bin/env bash
set -euo pipefail

# Use the project virtualenv Python by default; override with PYTHON if needed.
PYTHON="${PYTHON:-./higgs_audio_env/bin/python}"

"${PYTHON}" examples/generations_v2.py \
  --transcript examples/transcript/single_speaker/number.txt \
  --scene_prompt examples/scene_prompts/quiet_indoor.txt \
  --user_text examples/english-accent/script.txt \
  --user_voice examples/english-accent/japanese27.mp3 \
  --out_path test/test_jp_number.wav \
  --max_new_tokens 10000 \
  --chunk_method word \
  --rewrite_transcript \
  --chunk_max_word_num 400
