import logging
import sys
from functools import wraps


class AppLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        self.logger = logging.getLogger()

        if logging.getLogger("gunicorn.error").hasHandlers():
            self.logger = logging.getLogger("gunicorn.error")
        elif logging.getLogger("uvicorn").hasHandlers():
            self.logger = logging.getLogger("uvicorn")

        if self.logger.handlers:
            self.logger.handlers[0].setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)-8s [%(filename)s::%(funcName)s:%(lineno)d]\t %(message)s"
                )
            )

    def show_error(self, func):
        """Decorator to log exceptions with function arguments."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.info({"args": args, "kwargs": kwargs})
                self.logger.exception(e)

        return wrapper

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def exception(self, e, *args, **kwargs):
        self.logger.exception(e, *args, **kwargs)
