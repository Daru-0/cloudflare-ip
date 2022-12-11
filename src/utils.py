import logging
import os


def get_env(name: str, required: bool = False, default: str = None):
    value: str = os.environ.get(name, default)
    if required and value is None:
        logging.fatal(f"Environment variable {name} is required")
        exit(1)
    return value
