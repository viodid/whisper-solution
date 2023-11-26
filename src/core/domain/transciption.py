class Transcription:
    def __init__(self, status: int, id_audio: int, id_work: int, transcription_text: str):
        self.status = status
        self.idAudio = id_audio
        self.idWork = id_work
        self.transcription = transcription_text

    def __str__(self):
        return (f"Transcription, id_audio={self.id_audio}, id_work={self.id_work}, "
                f"transcription_text={self.transcription_text}")
