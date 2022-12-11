import datetime
import json
import os
import time
from smtplib import (SMTPAuthenticationError, SMTPConnectError,
                     SMTPRecipientsRefused, SMTPSenderRefused)

import requests
import yagmail

# Get environment variables
EMAIL =  os.getenv('EMAIL')
AUTH_KEY = os.getenv('AUTH_KEY')
RECORD_ID = os.getenv('RECORD_ID')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL'))
PUBLIC_IP_API_URL = "https://api.ipify.org?format=json"
ZONE_NAME = os.getenv('ZONE_NAME')
ZONE_ID = os.getenv('ZONE_ID')
CLOUDFLARE_URL = f"https://api.cloudflare.com/client/v4/zones/"
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')
RECEIVER_ADDRESS = os.getenv('RECEIVER_ADDRESS')

# Define constants
HEADER = {
	"X-Auth-Email": EMAIL, 
	"X-Auth-Key": AUTH_KEY,
	"content-type": "application/json"
	}

# Get the current time
def now():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Get the server's public IP
def get_public_ip():
	# Get the public IP of the server
	current_ip_json = requests.get(PUBLIC_IP_API_URL)
	# Status code should be 200, otherwise the API is probably down
	if current_ip_json.status_code != 200:
		print(f"[WARN] {now()} - Can't get current IP. Retrying...")
		time.sleep(10)
		current_ip_json = get_public_ip()
	return current_ip_json

# Send email
def send_email(email_body):
	content = "The public IP of the following record(s) has changed:\n\n"
	for record in email_body:
		content = content + record + "\n"
	try:
		with yagmail.SMTP(SENDER_ADDRESS, SENDER_PASSWORD) as server:
			server.send(
				to=RECEIVER_ADDRESS,
				subject="Public IP change",
				contents=content
			)
	except SMTPSenderRefused:
		print(f"[ERROR] {now()} - Can't send email. The sender address is invalid.")
	except SMTPAuthenticationError:
		print(f"[ERROR] {now()} - Can't send email. Check your credentials.")
	except SMTPRecipientsRefused:
		print(f"[ERROR] {now()} - Can't send email. Check your receiver address.")
	except SMTPConnectError:
		print(f"[ERROR] {now()} - Can't send email. Check your internet connection.")
	finally:
		print(f"[INFO] {now()} - Email sent.")

# Get the zone ID
def get_zone_id():
	zone_id = requests.get(CLOUDFLARE_URL , params={'name': ZONE_NAME}, headers=HEADER).json()['result'][0]['id']
	if not zone_id:
		print(f"[ERROR] {now()} - Can't get zone ID. Check your zone name.")
		exit(1)
	print(f"[INFO] {now()} - Zone ID for '{ZONE_NAME}': {zone_id}")
	return zone_id


def main():
	if ZONE_ID:
		zone_id = ZONE_ID
	else:
		zone_id = get_zone_id()
	# Looping forever
	while True:
		current_ip = get_public_ip().json()['ip']
		print(f"[INFO] {now()} - Current public IP is: {current_ip}")
		# Get all the A records or just the one selected
		if RECORD_ID:
			records = requests.get(CLOUDFLARE_URL + f"/{zone_id}/dns_records?type=A", headers=HEADER).json()
		else:
			records = requests.get(CLOUDFLARE_URL + f"/{zone_id}/dns_records/{RECORD_ID}", headers=HEADER).json()
		email_body = []
		for record in records['result']:
			print(f"[INFO] {now()} - Record \"{record['name']}\" IP: {record['content']}")
			# Change the IP using a PATCH request if the current IP is different from the one in the record
			if record['content'] != current_ip:
				payload = {"content": current_ip}
				requests.patch(CLOUDFLARE_URL + f"/{record['id']}", headers=HEADER, data=json.dumps(payload))
				print(f"[INFO] {now()} - Record \"{record['name']}\" updated to {current_ip}")
				email_body.append(f"Record \"{record['name']}\" from {record['content']} to {current_ip}")
		# Send email
		if SENDER_ADDRESS and SENDER_PASSWORD and RECEIVER_ADDRESS and len(email_body) > 0:
			print(f"[INFO] {now()} - Sending email...")
			send_email(email_body)
		# Wait before next check
		print(f"[INFO] {now()} - Wait {CHECK_INTERVAL} seconds before next check", end="\n-----\n")
		time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
	main()
