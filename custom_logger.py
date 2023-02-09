import logging


class CustomFormatter(logging.Formatter):
    # define colors for log levels
    grey = "\x1b[0;37m"
    light_blue = "\x1b[1;36m"
    yellow = "\x1b[1;33m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[1;32m"
    reset = "\x1b[0m"

    # log message format
    format = (
        "%(asctime)s.%(msecs)03d - [PROCESS %(process)d %(processName)s]"
        " - [THREAD %(thread)d %(threadName)s] - %(name)s - %(levelname)s - %(message)s"
    )

    # mapping of log levels to log message formats
    FORMATS = {
        logging.DEBUG: green + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)