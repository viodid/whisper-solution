import os
import whisper
import torch
import time


UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audios"))


def transcribe(files):
    output = {}
    # https://stackoverflow.com/questions/75775272/cuda-and-openai-whisper-enforcing-gpu-instead-of-cpu-not-working
    # https://stackoverflow.com/questions/75908422/whisper-ai-error-fp16-is-not-supported-on-cpu-using-fp32-instead
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(device)
    model = whisper.load_model('medium').to(device)

    for file in files:

        with open(os.path.join(UPLOAD_FOLDER, file.filename), "wb") as f:
            f.write(file.file.read())

        start = time.time()
        result = model.transcribe(os.path.join(UPLOAD_FOLDER, file.filename), word_timestamps=True)
        end = time.time()

        for message in result["segments"]:
            starttime = convertotime(message["start"])
            endtime = convertotime(message["end"])
            if file.filename in output:
                output[file.filename].append({"start": starttime, "end": endtime,
                                              "text": message["text"],
                                              "confidence": round_int_str(message["avg_logprob"]),
                                              "words_confidence": get_words_confidence(message["words"])
                                              })
            else:
                output[file.filename] = [{"start": starttime, "end": endtime,
                                          "text": message["text"],
                                          "confidence": round_int_str(message["avg_logprob"]),
                                          "words_confidence": get_words_confidence(message["words"])
                                          }]

        output[file.filename].append({"time": convertotime(end - start)})
        print(f"Transcription of {file.filename} completed")

        os.remove(os.path.join(UPLOAD_FOLDER, file.filename))

    return output


def convertotime(seconds):
    minutes, seconds = divmod(seconds, 60)
    formatted_time = f"{int(minutes):02}:{int(seconds):02}"

    return formatted_time


def get_words_confidence(words):
    words_confidence = []

    for word in words:
        words_confidence.append({"words": word["word"], "confidence": round_int_str(word["probability"])})

    return words_confidence


def round_int_str(number):
    string = str(round(number, 1) * 10).split('.', maxsplit=1)[0]
    return '_' + string
