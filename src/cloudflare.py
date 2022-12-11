from typing import List
import config
import json
import logging
import requests
import time

# Define constants
CLOUDFLARE_URL = f"https://api.cloudflare.com/client/v4/zones/"
PUBLIC_IP_API_URL = "https://api.ipify.org?format=json"

class Cloudflare:
    """Class for interacting with the Cloudflare API."""

    def __init__(self, cfg: config.Config):
        self.cfg = cfg

        self.header = {
            "X-Auth-Email": cfg.email,
            "X-Auth-Key": cfg.auth_key,
            "content-type": "application/json"
        }

        self.current_ip = self.get_public_ip()

        if (cfg.zone_id is not None):
            self.zone_id = cfg.zone_id
        else:
            self.zone_id = self.get_zone_id()

        if (cfg.record_id is not None):
            self.records = [cfg.record_id]
        else:
            self.records = self.get_records()

    def get_public_ip(self):
        """Get the public IP of the server."""
        
        logging.info(f"Getting current IP...")
        response = requests.get(PUBLIC_IP_API_URL)

        # Status code should be 200, otherwise the API is probably down
        if response.status_code != 200:
            logging.warning(f"Can't get current IP. Retrying...")
            time.sleep(10)
            response = self.get_public_ip()

        current_ip = response.json()['ip']
        logging.info(f"Current IP: {current_ip}")
        return current_ip

    def get_zone_id(self):
        """Get the zone ID."""

        logging.info(f"Getting zone ID...")
        response = requests.get(CLOUDFLARE_URL , params={'name': self.cfg.zone_name}, headers=self.header)

        if response.status_code != 200:
            logging.error(f"Can't get zone ID. Check your zone name.")
            exit(1)

        zone_id = response.json()['result'][0]['id']
        logging.info(f"Zone ID for '{self.cfg.zone_name}': {zone_id}")

        return zone_id

    def get_records(self):
        """Get the records of the zone."""

        response = requests.get(CLOUDFLARE_URL + self.zone_id + "/dns_records", headers=self.header)

        if response.status_code != 200:
            logging.error(f"Can't get records. Check your zone name.")
            exit(1)

        records = response.json()['result']
        logging.info(f"Records for '{self.cfg.zone_name}': {records}")

        return records

    def update_records(self):
        """Update the records of the zone."""

        updated_records = List[str]
        previous_ip: str

        for record in self.records:
            if record['type'] == 'A':
                if record['content'] != self.current_ip:
                    logging.info(f"Updating record '{record['name']}'...")
                    payload = {
                        "content": self.current_ip,
                    }
                    response = requests.patch(CLOUDFLARE_URL + self.zone_id + "/dns_records/" + record['id'], headers=self.header, data=json.dumps(payload))

                    if response.status_code != 200 or response.json()['success'] is False:
                        logging.error(f"Can't update record '{record['name']}'.")

                    logging.info(f"Record '{record['name']}' updated.")
                    updated_records.append(record['name'])
                    previous_ip = record['content']

                logging.info(f"Record '{record['name']}' is up to date.")
        
        return updated_records, previous_ip
