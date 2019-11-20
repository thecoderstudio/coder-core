import unittest


class TestEncrypt(unittest.TestCase):
    def test_hash_HMAC_hex(self):
        from invytecore.lib.encrypt import hash_HMAC_hex

        message_1 = b"teststring1"
        message_2 = b"teststring2"
        key_1 = b"sgfdgsdgdf"
        key_2 = b"fsdhffdhdf"

        hash_1 = hash_HMAC_hex(message_1, key_1)
        hash_1_duplicate = hash_HMAC_hex(message_1, key_1)
        hash_1_different_key = hash_HMAC_hex(message_1, key_2)
        hash_2 = hash_HMAC_hex(message_2, key_1)

        self.assertEqual(hash_1, hash_1_duplicate)
        self.assertNotEqual(hash_1, hash_1_different_key)
        self.assertNotEqual(hash_1, hash_2)

    def test_get_small_secure_token_success(self):
        from invytecore.lib.encrypt import get_small_secure_token

        token_1 = get_small_secure_token()
        token_2 = get_small_secure_token()

        self.assertEqual(len(token_1), 6)
        self.assertEqual(len(token_2), 6)
        self.assertNotEqual(token_1, token_2)

    def test_get_secure_token_success(self):
        from invytecore.lib.encrypt import get_secure_token

        token_1 = get_secure_token()
        token_2 = get_secure_token()

        self.assertEqual(len(token_1), 64)
        self.assertEqual(len(token_2), 64)
        self.assertNotEqual(token_1, token_2)
