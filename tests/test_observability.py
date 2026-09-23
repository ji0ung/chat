import json
import logging
import unittest

from app.config import Settings
from app.observability import JsonFormatter, PrivacyFilter


class ObservabilityTests(unittest.TestCase):
    def test_json_formatter_produces_structured_event(self) -> None:
        record = logging.LogRecord("test", logging.INFO, "", 0, "fallback", (), None)
        record.event = "memory_recalled"
        record.fields = {"result_count": 2, "duration_ms": 4.2}
        payload = json.loads(JsonFormatter().format(record))
        self.assertEqual(payload["event"], "memory_recalled")
        self.assertEqual(payload["result_count"], 2)

    def test_content_is_redacted_by_default(self) -> None:
        privacy = PrivacyFilter(Settings(log_include_content=False, log_hash_salt="test"))
        fields = privacy.text_fields("나는 민트초코를 좋아해")
        self.assertNotIn("message_content", fields)
        self.assertEqual(fields["message_length"], 12)
        self.assertIn("message_sha256", fields)

    def test_identifier_hash_is_stable_and_salted(self) -> None:
        first = PrivacyFilter(Settings(log_hash_salt="a")).hash_identifier("user-1")
        second = PrivacyFilter(Settings(log_hash_salt="a")).hash_identifier("user-1")
        other = PrivacyFilter(Settings(log_hash_salt="b")).hash_identifier("user-1")
        self.assertEqual(first, second)
        self.assertNotEqual(first, other)


if __name__ == "__main__":
    unittest.main()
