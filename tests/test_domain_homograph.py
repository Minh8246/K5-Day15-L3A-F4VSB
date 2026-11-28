import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codebase"))

from agent import answer
from ai import HIGH_RISK
from tools import check_domain_rules, extract_message_signals, lookup_official_channels


class DomainHomographTests(unittest.TestCase):
    def setUp(self):
        model = patch("agent.call_model", return_value={"text": HIGH_RISK})
        model.start()
        self.addCleanup(model.stop)

    def test_official_apple_domain_remains_uncertain(self):
        result = answer("Apple: Xem thông báo tại https://www.apple.com")["output"]
        self.assertTrue(result.startswith("CHƯA ĐỦ CĂN CỨ"))
        self.assertNotIn("R_DOMAIN_HOMOGRAPH", result)

    def test_lookalike_warns_in_both_encodings(self):
        for host in ("аррӏе.com", "xn--80ak6aa92e.com"):
            with self.subTest(host=host):
                result = answer(f"Apple: Xem thông báo tại https://www.{host}")["output"]
                self.assertTrue(result.startswith("CÓ DẤU HIỆU RỦI RO CAO"))
                self.assertIn("[R_DOMAIN_HOMOGRAPH]", result)
                self.assertIn("trông giống apple.com", result)
                self.assertIn("Tự xác minh", result)

    def test_legitimate_idn_remains_uncertain_even_if_model_returns_high(self):
        for host in ("öbb.at", "xn--bb-eka.at"):
            with self.subTest(host=host):
                result = answer(f"Xem thông báo tại https://{host}")["output"]
                self.assertTrue(result.startswith("CHƯA ĐỦ CĂN CỨ"))
                self.assertNotIn("R_DOMAIN_HOMOGRAPH", result)

    def test_invalid_punycode_does_not_break_analysis(self):
        result = answer("Xem thông báo tại https://xn--.example.invalid")["output"]
        self.assertTrue(result.startswith("CHƯA ĐỦ CĂN CỨ"))
        self.assertNotIn("R_DOMAIN_HOMOGRAPH", result)

    def test_financial_domain_match_handles_labels_and_remains_strict(self):
        for host, expected_mismatch in (
            ("hỗtrợ.vietcombank.com.vn", False),
            ("vietcombank。com。vn", False),
            ("vietcombank.com.vn.example.invalid", True),
        ):
            with self.subTest(host=host):
                signals = extract_message_signals(f"Vietcombank: Xem thông báo tại https://{host}")
                official = lookup_official_channels(signals["organization"])
                findings = check_domain_rules(signals, official)["findings"]
                rules = {finding["id"] for finding in findings}
                self.assertEqual("R_DOMAIN_MISMATCH" in rules, expected_mismatch)


if __name__ == "__main__":
    unittest.main()
