import os
from tika import parser

from .file_data import FileData

import warnings
warnings.filterwarnings('ignore')

def parse_file(file_path) -> FileData:
    try:
        results = parser.from_file(file_path)

        metadata=results['metadata'] # TODO: Cleanup metadata
        content=results['content']

        if content is not None:
            content = content.strip()
        else:
            content = ''
            print(f"Content not available for file {file_path}")

        return FileData(file_path=file_path, content=content, metadata=metadata)
    except Exception as e:
        print(f"An error occurred while parsing '{file_path}': {e}")
        raise e
