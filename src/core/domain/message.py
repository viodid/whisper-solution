class Message:
    def __init__(self, id_audio: int, id_work: int, audio_name: str, container_name: str):
        self.id_audio = id_audio
        self.id_work = id_work
        self.audio_name = audio_name
        self.container_name = container_name

    def __str__(self):
        return (f"Message, id_audio={self.id_audio}, id_work={self.id_work}, "
                f"transcription_text={self.audio_name}")
