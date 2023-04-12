import unittest
import notification
import cloudflare
import config

class TestNotification(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = config.Config()
        self.cf = cloudflare.Cloudflare(self.cfg)
        self.notif = notification.Notification(self.cfg)

        self.current_ip = self.cf.get_public_ip()
        self.records = [str]
        for record in self.cf.get_records():
            if record['type'] == "A":
                self.records.append(record['name'])

    def test_send_notification(self):
        self.notif.send_notification(self.records, self.current_ip, self.current_ip)