import logging
import logging.config

from colorlog import ColoredFormatter


class Log():
    __instance = None
    __verbose: bool = False

    def __new__(cls, verbose: bool = False):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__verbose = verbose
            cls.__init_logging()

        return cls.__instance

    @classmethod
    def __init_logging(cls) -> None:
        logging.config.fileConfig('logging.conf')

        logger = logging.getLogger()

        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                if cls.__verbose:
                    handler.setLevel(level=logging.DEBUG)

                formatter = ColoredFormatter(
                    handler.formatter._fmt,
                    datefmt=handler.formatter.datefmt,
                    reset=True,
                    log_colors={
                        'DEBUG': 'cyan',
                        'INFO': 'green',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'red,bg_white',
                    },
                )
                handler.setFormatter(formatter)

    @classmethod
    def info(cls, message: str) -> None:
        logging.getLogger().info(message)

    @classmethod
    def debug(cls, message: str) -> None:
        logging.getLogger().debug(message)

    @classmethod
    def warn(cls, message: str) -> None:
        logging.getLogger().warning(message)

    @classmethod
    def error(cls, message: str) -> None:
        logging.getLogger().error(message)

    @classmethod
    def critical(cls, message: str) -> None:
        logging.getLogger().critical(message)

    @classmethod
    def is_verbose(cls) -> bool:
        return cls.__verbose
