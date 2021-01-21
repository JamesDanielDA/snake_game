import logging


class GameLogger(logging):
    """
    Set up the logger for each module creating an object of this class
    """
    def __init__(file_dunder, log_filename):
        super().__init__()
        logger = logging.getLogger(file_dunder)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s:%(messages)s")

        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)