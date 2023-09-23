from utils.logger import log

from tika import parser
import os
from db.file import FileData

def parse_file(file_path) -> FileData:
    try:
        results = parser.from_file(file_path)

        metadata=results['metadata'] # TODO: Cleanup metadata
        content=results['content']

        if content is not None:
            content = content.strip()
        else:
            content = ''
            log.info(f"Content not available for file {file_path}")

        metadata = extract_metadata(metadata)

        return FileData(file_id=None, file_path=file_path, content=content), metadata
    except Exception as e:
        log.error(f"An error occurred while parsing '{file_path}': {e}")
        raise e

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