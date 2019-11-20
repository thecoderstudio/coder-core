import base64
import binascii

import bcrypt
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256

from codercore.lib.encrypt.padding import pad, unpad


def hash_plaintext(plaintext):
    salt = bcrypt.gensalt()
    return (bcrypt.hashpw(plaintext.encode('utf-8'), salt).decode('utf-8'),
            salt.decode('utf-8'))


def encrypt_string_AES(string_message, key, iv):
    """Encrypts a string using AES and returns the encrypted string."""
    return base64.b64encode(
        encrypt_AES(string_message.encode(), key, iv)
    ).decode()


def decrypt_string_AES(encrypted_string_message, key, iv):
    """Decrypts a string using AES and returns the decrypted string."""
    return decrypt_AES(
        base64.b64decode(encrypted_string_message.encode()), key, iv
    ).decode()


def encrypt_AES(bytes_message, key, iv):
    """Encrypts a bytes string using AES and returns the encrypted bytes."""
    encrypt_client = AES.new(key, AES.MODE_CBC, iv)
    encrypted_bytes_string = encrypt_client.encrypt(
        pad(bytes_message, AES.block_size))
    return encrypted_bytes_string


def decrypt_AES(bytes_message, key, iv):
    """Decrypts a bytes string using AES and returns the decrypted bytes."""
    decrypt_client = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = decrypt_client.decrypt(bytes_message)
    try:
        return unpad(decrypted_message, AES.block_size)
    except ValueError:
        # Presume message was unpadded
        return decrypted_message


def decrypt_secret(secret, key, iv):
    decoded_secret = base64.b64decode(secret.encode('utf-8'))
    return decrypt_AES(decoded_secret, key, iv).decode('utf-8')


def get_small_secure_token():
    return binascii.b2a_hex(Random.get_random_bytes(3)).decode('utf-8')


def get_secure_token():
    return binascii.b2a_hex(Random.get_random_bytes(32)).decode('utf-8')


def hash_HMAC_hex(message, key):
    return HMAC.new(key, message, SHA256.new()).hexdigest()


def compare_plaintext_to_hash(plaintext, hashed_plaintext=None, salt=None):
    """Checks the plaintext against given hashed bytes.

    Even if no hashed_plaintext is given we hash the plaintext with a
    generated salt. This will of course throw a AttributeError that needs to be
    handled accordingly.
    """

    if not salt:
        salt = bcrypt.gensalt().decode('utf-8')

    new_hashed_plaintext = bcrypt.hashpw(plaintext.encode('utf-8'),
                                         salt.encode('utf-8'))

    try:
        if new_hashed_plaintext == hashed_plaintext.encode('utf-8'):
            return True
    except AttributeError:
        # hashed_plaintext not given, should return False
        pass

    return False
