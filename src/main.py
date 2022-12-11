import cloudflare
import config
import logging
import notification
import time

def main():
	logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

	logging.info(f"Starting Cloudflare DNS Auto Updater...")

	# Initializing classes
	logging.info("Fetching configuration...")
	cfg = config.Config()
	cf = cloudflare.Cloudflare(cfg)
	notify = notification.Notification(cfg)

	# Looping forever
	while True:
		updated_records, previous_ip = cf.update_records()

		if len(updated_records) > 0:
			notify.send_notification(updated_records, previous_ip, cf.current_ip)

		logging.info(f"Wait {cfg.check_interval} seconds before next check")
		time.sleep(cfg.check_interval)
		cf.current_ip = cf.get_public_ip()


if __name__ == '__main__':
	main()
