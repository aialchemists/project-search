from utils.logger import log
from utils.configs import DATA_DIR

import json

from tika import parser
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import whisper

from db.file import FileData
from utils.torch import get_device
from utils.file import detect_file_type, FileType, extract_metadata

image_model: BlipForConditionalGeneration
image_processor: BlipProcessor
audio_model: whisper.Whisper

# TODO: Make this a configuration
IMAGE_MODEL_ID = "Salesforce/blip-image-captioning-large"

def init():
    # Instantiate the BLIP image model
    device = get_device()

    global image_model
    image_model = BlipForConditionalGeneration.from_pretrained(IMAGE_MODEL_ID).to(device)
    global image_processor
    image_processor = BlipProcessor.from_pretrained(IMAGE_MODEL_ID)

    # Instantiate Whisper audio model
    global audio_model
    audio_model = whisper.load_model("large").to(device)

def parse_file(file_path) -> tuple[FileData, dict]:
    try:
        content = None

        file_type = detect_file_type(file_path)
        if file_type == FileType.TEXT:
            content = parse_text(file_path)
        elif file_type == FileType.IMAGE:
            content = parse_image(file_path)
        elif file_type == FileType.AUDIO:
            content = parse_audio(file_path)
        elif file_type == FileType.VIDEO:
            content = parse_video(file_path)

        results = parser.from_file(file_path)
        metadata = extract_metadata(results['metadata'])

        file_path = file_path.replace(DATA_DIR, '')

        return FileData(file_type=file_type, file_path=file_path, content=json.dumps(content)), metadata
    except Exception as e:
        log.error(f"An error occurred while parsing '{file_path}': {e}")
        raise e

def parse_text(file_path):
    # Extract text from pdf
    results = parser.from_file(file_path)
    content = results['content']

    if content is not None:
        content = content.strip()
    else:
        content = ''
        log.info(f"Content not available for file {file_path}")

    return content

def parse_image(file_path):
    # Generate caption as content from image
    image = Image.open(file_path).convert('RGB')
    inputs = image_processor(image, return_tensors="pt")
    out = image_model.generate(**inputs, max_new_tokens=100)
    caption = image_processor.decode(out[0], skip_special_tokens=True)
    return caption

def parse_audio(file_path):
    # Transcribe the audio as content
    audio_transcription = audio_model.transcribe(file_path)

    content = []

    for segment in audio_transcription['segments']:
        content.append({
            "text": segment['text'],
            "start_time": segment['start'] * 1000,
            "end_time": segment['end'] * 1000
        })

    return content

def parse_video(file_path):
    return parse_audio(file_path)
