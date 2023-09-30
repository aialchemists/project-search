from enum import Enum

import magic

class FileType(str, Enum):
    TEXT = 'text'
    IMAGE = 'image'
    AUDIO = 'audio'
    VIDEO = 'video'
    UNKNOWN = 'unknown'

def detect_file_type(file_path) -> FileType:
    # Create a magic object to detect file type
    mime = magic.Magic(mime=True)
    file_mime = mime.from_file(file_path)
    
    if file_mime.startswith("text/") or file_mime.startswith("application/pdf") \
        or file_mime.startswith("application/msword") or file_mime.startswith("text/html"):
        return FileType.TEXT
    elif file_mime.startswith("image"):
        return FileType.IMAGE
    elif file_mime.startswith("audio"):
        return FileType.AUDIO
    elif file_mime.startswith("video"):
        return FileType.VIDEO
    else:
        return FileType.UNKNOWN

def extract_metadata(metadata):
    # Extracting specific metadata fields
    created_date = metadata.get('dcterms:created', '')
    year = created_date.split('-')[0]

    # Get file type
    resource_name = metadata.get('resourceName', '')[2:-1]
    file_extension = os.path.splitext(resource_name)[1]
    file_extension = file_extension[1:] if file_extension else ""

    author = metadata.get('dc:creator', '')

    language = metadata.get('dc:language', '')

    return {
        'year': year,
        'file_format': file_extension,
        'author': author,
        'language': language
    }
