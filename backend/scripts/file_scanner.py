from utils.logger import log
import os

from utils.configs import DATA_DIR

from tasks.extract import parse_task

def scan_local_dir(directory_path):
    log.info(f"Scaning files in dir {directory_path}")
    if os.path.isdir(directory_path):
        file_paths = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, filename))]
        for path in file_paths:
            if not os.path.basename(path).startswith("."):
                parse_task.delay(path)

        log.info(f"Found {len(file_paths)} files. Tasks scheduled.")
    else:
        log.error(f"'{directory_path}' is not a valid directory path.")

scan_local_dir(DATA_DIR)
