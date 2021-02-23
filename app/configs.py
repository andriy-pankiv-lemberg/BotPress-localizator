import os
import sys
from dotenv import load_dotenv
load_dotenv()


class TranslateDB:
    HOST = os.getenv('TRANSLATE_RESULT_DB_HOST')
    PORT = os.getenv('TRANSLATE_RESULT_DB_PORT')
    NAME = os.getenv('TRANSLATE_RESULT_DB_NAME')
    USER = os.getenv('TRANSLATE_RESULT_DB_USER')
    PASSWORD = os.getenv('TRANSLATE_RESULT_DB_PASSWORD')


class SupervisorConfig:
    SERVICE_BUS_CONFIRMATION_TIMEOUT = int(os.getenv('SERVICE_BUS_CONFIRMATION_TIMEOUT', 300))
    COUGH_NOTIFICATION_TIMEOUT = int(os.getenv('COUGH_NOTIFICATION_TIMEOUT', 300))
    NUM_OF_WORKERS = int(os.getenv('NUM_OF_WORKERS', 20))
    STORAGE_PATH = os.path.join('/cough-audio-supervisor', 'storage')
