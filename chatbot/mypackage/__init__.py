# chatbot/__init__.py

from .microphone import Microphone, Recognizer
from .audio import AudioData
from .exceptions import WaitTimeoutError
from .recog_whisper import recog_whisper

__version__ = "1.0.0"
__author__ = "Dev Jayesh Patel"

