import os
import dotenv

dotenv.load_dotenv()


class Config:
    """Set Flask configuration vars from .env file."""
    WHISPER_MODEL = os.getenv('WHISPER_MODEL') or 'base'
    ROOT = os.path.dirname(os.path.join(os.path.dirname(__file__), "../"))
    AUDIOS_PATH = os.path.abspath(os.path.join(ROOT, "static/audios"))
    SERVICE_BUS_CONNECTION_STRING = os.getenv('SERVICE_BUS_CONNECTION_STRING')
    SERVICE_BUS_QUEUE_NAME = os.getenv('SERVICE_BUS_QUEUE_NAME')
    AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    DISPATCHER_URL = os.getenv('DISPATCHER_URL')
