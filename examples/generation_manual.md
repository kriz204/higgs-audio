# generation.py Manual

This manual documents `examples/generation.py`, an example script for generating speech audio using the HiggsAudio model.

**Overview**
- **Purpose:**: Convert text (or a transcript) into speech using a pretrained HiggsAudio generation model.
- **Location:**: `examples/generation.py`

**Requirements**
- **Python packages:**: See `requirements.txt` and `pyproject.toml` for required packages (notably `torch`, `transformers`, `soundfile`, `click`, `loguru`).
- **Audio tokenizer:**: A compatible HiggsAudio audio tokenizer (default: `bosonai/higgs-audio-v2-tokenizer`).

**Quick Start**
- **Basic generation (use defaults):**
```bash
python examples/generation.py
```

- **Custom model and output path:**
```bash
python examples/generation.py --model_path bosonai/higgs-audio-v2-generation-3B-base --out_path my_generation.wav
```

- **Use a local transcript file and scene prompt:**
```bash
python examples/generation.py --transcript examples/transcript/single_speaker/en_dl.txt --scene_prompt examples/scene_prompts/quiet_indoor.txt --out_path out.wav
```

**Main CLI Options**
- **`--model_path`**: Path or HF repo id of the pretrained model. Default: `bosonai/higgs-audio-v2-generation-3B-base`.
- **`--audio_tokenizer`**: Path or repo id for the audio tokenizer. Default: `bosonai/higgs-audio-v2-tokenizer`.
- **`--max_new_tokens`**: Maximum new tokens to generate (int). Default: `2048`.
- **`--transcript`**: Path to transcript text file or a direct prompt string. Default: `transcript/single_speaker/en_dl.txt`.
- **`--scene_prompt`**: Path to a scene prompt file or `empty` for no scene prompt. Default: `examples/scene_prompts/quiet_indoor.txt`.
- **`--temperature`**: Sampling temperature (float). Default: `1.0`.
- **`--top_k`**: Top-k sampling (int). Default: `50`.
- **`--top_p`**: Top-p (nucleus) sampling (float). Default: `0.95`.
- **`--ras_win_len`** and **`--ras_win_max_num_repeat`**: Options controlling RAS sampling window and repeats. Defaults: `7` and `2`.
- **`--tone_url`**: Path to a tone description text file to influence voice style.
- **`--user_voice`**, **`--user_text`**: For voice cloning/single-speaker mode: `user_voice` is a `.wav` file (path) and `user_text` is the transcript text file used to reference that voice. Provide both to enable voice-cloning behavior.
- **`--chunk_method`**: `None`, `speaker`, or `word`. Controls how the input transcript is split. Default: `None`.
- **`--chunk_max_word_num`**: When `--chunk_method=word`, maximum words per chunk (default 200).
- **`--chunk_max_num_turns`**: When `--chunk_method=speaker`, max turns per chunk (default 1).
- **`--generation_chunk_buffer_size`**: How many previously-generated chunks to keep in memory (helps control context size).
- **`--seed`**: Random seed (int).
- **`--device_id`**: CUDA device id (int). If not set, the script picks the best device.
- **`--device`**: `auto|cuda|mps|none` — choose device. `auto` prefers CUDA, then MPS, then CPU.
- **`--use_static_kv_cache`**: Use static KV cache (faster on CUDA). Default: `1` (enabled).
- **`--out_path`**: Output WAV file path. Default: `generation.wav`.

**Inputs and Formats**
- **Transcript (`--transcript`)**: Plain UTF-8 text. The script performs basic normalization and will append a final sentence terminator if missing.
- **Scene prompt (`--scene_prompt`)**: A text file describing acoustic scene or context. If set to `empty` or not provided, scene description is omitted.
- **User voice (`--user_voice`)**: A `.wav` file used as a voice reference. When provided together with `--user_text` the script encodes the audio and includes it in context for voice cloning.
- **User text (`--user_text`)**: Plain text transcript corresponding to the `--user_voice` audio sample. Both must exist or an error is raised.

**Chunking behavior**
- **None**: The whole transcript is sent as a single prompt (default).
- **`speaker`**: Splits text by speaker tags such as `[SPEAKER0]` and groups turns; useful for multi-speaker dialogues.
- **`word`**: Splits by word count (language-aware for Chinese using `jieba`). Configure `--chunk_max_word_num`.

**Single-speaker vs Multi-speaker**
- The script includes helpers to prepare context for either mode. For single-speaker voice cloning use `--user_voice` + `--user_text` and optionally `--tone_url`. For multi-speaker scenarios include speaker tags like `[SPEAKER0]` in the transcript or specify multiple `ref_audio` entries (internal helpers).

**Device selection & performance**
- The script auto-selects CUDA if available. For Apple Silicon, `mps` is supported but static KV cache is disabled on MPS. If you manually set `--device_id`, CUDA is assumed.
- Use `--use_static_kv_cache 1` on CUDA to improve throughput for repeated runs.

**Output**
- The generated audio is written as a WAV at the sample rate used by the tokenizer (default SR = 24000). Location is `--out_path`.

**Troubleshooting**
- File not found for `--user_voice` or `--user_text`: Verify path and that the file exists. The script raises `FileNotFoundError` if missing.
- High memory usage / OOM on GPU: Try reducing `--max_new_tokens`, reduce model size, or disable static KV cache.
- MPS specific issues: Static KV cache and CUDA graphs are not supported — `--use_static_kv_cache` will be ignored for MPS.

**Useful examples**
- Voice cloning with a reference sample:
```bash
python examples/generation.py --user_voice examples/voice_prompts/belinda.wav --user_text examples/voice_prompts/belinda.txt --out_path belinda_out.wav
```

- Chunked speaker dialogue generation:
```bash
python examples/generation.py --transcript examples/transcript/multi_speaker/sample.txt --chunk_method speaker --out_path dialogue_out.wav
```

**Next steps**
- If you want, I can add a short example transcript file, or create a small wrapper script that runs the example with commonly used options.

**Contact**
- For questions about this manual or the example, reply with requested changes.
