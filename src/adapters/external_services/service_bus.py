from azure.servicebus import ServiceBusClient
from src.adapters.external_services.blob_storage import BlobStorage
from src.core.domain.message import Message
from src.core.domain.transciption import Transcription
from src.core.use_cases.transcribe import transcribe
import logging
import requests
from config.config import Config
import os
import json

logging.basicConfig(level=logging.WARNING, filename=Config.ROOT + "/logs/logs.log", datefmt='%Y-%m-%d %H:%M:%S')


class ServiceBus:
    def __init__(self, conn: str, queue: str):
        self.conn = conn
        self.queue = queue

    def get_from_queue(self):
        with ServiceBusClient.from_connection_string(self.conn) as client:
            with client.get_queue_receiver(queue_name=self.queue) as receiver:
                msg = receiver.next()
                print(msg)
                message = json.loads(msg.__str__())
                msg_obj = Message(id_audio=message.get('idAudio'),
                                  id_work=message.get('idWork'),
                                  audio_name=message.get('audioName'),
                                  container_name=message.get('containerName'))
                blob_storage = BlobStorage(conn=Config.AZURE_STORAGE_CONNECTION_STRING,
                                           container=msg_obj.container_name)
                try:
                    blob_storage.download_blob(msg_obj.audio_name, os.path.join(Config.AUDIOS_PATH, msg_obj.audio_name))
                except Exception as e:
                    print(f"Unable to download blob {msg_obj.audio_name}, error: {e}")
                    logging.error(f"Unable to download blob {msg_obj.audio_name}, error: {e}")

                transcription_text = transcribe(msg=msg_obj)

                transcription_obj = Transcription(status=200,
                                                  id_audio=msg_obj.id_audio,
                                                  id_work=msg_obj.id_work,
                                                  transcription_text=transcription_text)

                try:
                    requests.post(url=Config.DISPATCHER_URL, json=transcription_obj.__dict__, headers={
                        "Content-Type": "application/json"
                    })
                except Exception as e:
                    print(f"Unable to send transcription to dispatcher, error: {e}")
                    logging.error(f"Unable to send transcription to dispatcher, error: {e}")

                blob_storage.remove_blob(blob_name=msg_obj.audio_name)

                os.remove(os.path.join(Config.AUDIOS_PATH, msg_obj.audio_name))

                receiver.complete_message(msg)

                print(f"Message {msg_obj.audio_name} processed successfully")
