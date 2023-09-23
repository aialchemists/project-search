from utils.logger import log

from tika import parser

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

        return FileData(file_id=None, file_path=file_path, content=content)
    except Exception as e:
        log.error(f"An error occurred while parsing '{file_path}': {e}")
        raise e
