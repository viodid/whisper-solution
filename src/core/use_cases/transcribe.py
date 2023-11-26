import whisper
import torch
import os
from config.config import Config


def transcribe(msg):
    output = []
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = whisper.load_model(Config.WHISPER_MODEL).to(device)

    try:
        result = model.transcribe(os.path.join(Config.AUDIOS_PATH, msg.audio_name), word_timestamps=True)
    except Exception as e:
        return {
            "status": False,
            "description": f"Error in transcribing audio: {e}"
        }

    for message in result["segments"]:
        output.append(message["text"])

    return ''.join(output)
