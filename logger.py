import logging


class GameLogger:
    """
    Set up the logger for each module creating an object of this class
    """
    def __init__(self, file_dunder_name:str,
                        logger_level:'logging.level' = logging.DEBUG, 
                        file_handler_name:str = None, 
                        file_level:'logging.level' = logging.INFO) -> None:

        self.logger = logging.getLogger(file_dunder_name)
        self.logger.setLevel(logger_level)
        self.formatter = logging.Formatter("%(asctime)s: %(name)s: %(message)s")

        if file_handler_name == None:
            file_handler_name = 'logs/' + file_dunder_name + '.log'
        self.file_handler = logging.FileHandler(file_handler_name)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)