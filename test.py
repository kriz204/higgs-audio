from boson_multimodal.serve.serve_engine import HiggsAudioServeEngine, HiggsAudioResponse
from boson_multimodal.data_types import ChatMLSample, Message, AudioContent

import torch
import torchaudio
import time
import click
import base64

MODEL_PATH = "bosonai/higgs-audio-v2-generation-3B-base"
AUDIO_TOKENIZER_PATH = "bosonai/higgs-audio-v2-tokenizer"

audio_file_path = "./input.wav"

system_prompt = (
    "Generate audio following instruction.\n\n<|scene_desc_start|>\nShe speaks with a calm, gentle, and informative tone at a measured pace, with excellent articulation and very clear audio. She naturally brings storytelling to life with an articulate, genuine, and personable vocal style\n<|scene_desc_end|>\n"
)

def encode_base64_content_from_file(file_path: str) -> str:
    """Encode a content from a local file to base64 format."""
    # Read the file as binary and encode it directly to Base64
    with open(file_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
    return audio_base64


voice_sample_audio = encode_base64_content_from_file(audio_file_path)

messages = [
    Message(
        role="system",
        content=system_prompt,
    ),

    Message(
        role="user",
        content="The sun rises in the east and sets in the west. This simple fact has been observed by humans for thousands of years.",
    ),
]
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {device}")

serve_engine = HiggsAudioServeEngine(MODEL_PATH, AUDIO_TOKENIZER_PATH, device=device)

output: HiggsAudioResponse = serve_engine.generate(
    chat_ml_sample=ChatMLSample(messages=messages),
    max_new_tokens=1024,
    temperature=0.3,
    top_p=0.95,
    top_k=50,
    stop_strings=["<|end_of_text|>", "<|eot_id|>"],
)
torchaudio.save(f"output4.wav", torch.from_numpy(output.audio)[None, :], output.sampling_rate)
