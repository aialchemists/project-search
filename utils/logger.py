import logging

# Creating this util as default log level is warning
log = logging.getLogger("VS Logger")
log.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

def print_line():
    print('─' * 100)
