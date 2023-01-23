import logging
import utils

class Config(object):
    """Configuration class for the application."""
    def __init__(self):
        self.auth_key = utils.get_env("AUTH_KEY", required=True)
        logging.debug(f"Auth key: {self.auth_key}")
        self.check_interval = int(utils.get_env("CHECK_INTERVAL", required=False, default="86400"))
        logging.debug(f"Check interval: {self.check_interval}")
        self.email = utils.get_env("EMAIL", required=True)
        logging.debug(f"Email: {self.email}")
        self.receiver_address = utils.get_env("RECEIVER_ADDRESS", required=False)
        logging.debug(f"Receiver address: {self.receiver_address}")
        self.record_id = utils.get_env("RECORD_ID", required=False)
        logging.debug(f"Record ID: {self.record_id}")
        self.sender_address = utils.get_env("SENDER_ADDRESS", required=False)
        logging.debug(f"Sender address: {self.sender_address}")
        self.sender_password = utils.get_env("SENDER_PASSWORD", required=False)
        logging.debug(f"Sender password: {self.sender_password}")
        self.zone_id = utils.get_env("ZONE_ID", required=False)
        logging.debug(f"Zone ID: {self.zone_id}")
        self.zone_name = utils.get_env("ZONE_NAME", required=False)
        logging.debug(f"Zone name: {self.zone_name}")
        if (self.zone_id is None and self.zone_name is None):
            logging.fatal("Either ZONE_ID or ZONE_NAME must be set")
            exit(1)
