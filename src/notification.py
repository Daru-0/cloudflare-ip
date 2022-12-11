from smtplib import (SMTPAuthenticationError, SMTPConnectError,
                     SMTPRecipientsRefused, SMTPSenderRefused)
from typing import List
import config
import logging
import yagmail

class Notification:
    def __init__(self, cfg: config.Config):
        self.cfg = cfg
        if cfg.sender_address is not None and cfg.sender_password is not None and cfg.receiver_address is not None:
            self.smtp = yagmail.SMTP(cfg.sender_address, cfg.sender_password)
        else:
            self.smtp = None

    def send_notification(self, records: List[str], previous_ip: str, current_ip: str):
        if self.smtp is not None:
            logging.info(f"Sending email...")
            self.send_email(records, previous_ip, current_ip)

    def send_email(self, records: List[str], previous_ip: str, current_ip: str):
        content = f'The public IP of the following record(s) has changed from {previous_ip} to {current_ip}:\n\n'
        for record in records:
            content = content + "- " + record + "\n"
        try:
            self.smtp.send(
                to=self.cfg.receiver_address,
                subject="Public IP change",
                contents=content
            )
        except SMTPSenderRefused:
            logging.error(f"Can't send email. The sender address is invalid.")
        except SMTPAuthenticationError:
            logging.error(f"Can't send email. Check your credentials.")
        except SMTPRecipientsRefused:
            logging.error(f"Can't send email. Check your receiver address.")
        except SMTPConnectError:
            logging.error(f"Can't send email. Check your internet connection.")
        finally:
            logging.info(f"Email sent.")
