import unittest

from app import validate_email


class ValidateEmailTests(unittest.TestCase):
    def test_accepts_valid_email(self):
        self.assertTrue(validate_email("farmer@example.com"))

    def test_rejects_invalid_email(self):
        self.assertFalse(validate_email("farmer-at-example.com"))


if __name__ == "__main__":
    unittest.main()
