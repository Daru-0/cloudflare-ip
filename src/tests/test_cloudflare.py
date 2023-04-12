import unittest
import cloudflare
import config
import re

class TestCloudflare(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = config.Config()
        self.cf = cloudflare.Cloudflare(self.cfg)

    def test_get_public_ip(self):
        self.assertTrue(re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", self.cf.get_public_ip()))

    def test_get_zone_id(self):
        self.assertTrue(re.match(r"\w{32}", self.cf.get_zone_id()))

    def test_get_records(self):
        self.assertGreater(len(self.cf.get_records()), 0)

    def test_update_records_no_update(self):
        record = self.cf.get_records()[0]
        self.cf.current_ip = record['content']
        self.assertEqual(len(self.cf.update_records()), 0)
        