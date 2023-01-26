import pytest

from codercore.lib.hash import bcrypt_check_plaintext_equals_hash, bcrypt_hash

PASSWORD_HASH = "$2b$12$50eN8MSIm9KDRpzmGL4JQO9gGy.2MDAafSOtqu9mZwfkb7jh33j26"
PASSWORD_SALT = "$2b$12$50eN8MSIm9KDRpzmGL4JQO"


def test_bcrypt_hash():
    password_hash, _ = bcrypt_hash("password", PASSWORD_SALT.encode("utf-8"))

    assert password_hash == PASSWORD_HASH

    password_hash, _ = bcrypt_hash("password")

    assert password_hash != PASSWORD_HASH


def test_bcrypt_hash_no_salt_different_outcome():
    password_hash, _ = bcrypt_hash("password")
    password_hash_2, _ = bcrypt_hash("password")

    assert password_hash != password_hash_2


def test_bcrypt_check_plaintext_equals_hash():
    assert (
        bcrypt_check_plaintext_equals_hash("password", PASSWORD_HASH, PASSWORD_SALT)
        is True
    )
    assert (
        bcrypt_check_plaintext_equals_hash("fakepassword", PASSWORD_HASH, PASSWORD_SALT)
        is False
    )


def test_bcrypt_check_plaintext_equals_hash_no_password():
    with pytest.raises(AttributeError):
        bcrypt_check_plaintext_equals_hash(None, "hash", "salt")


def test_bcrypt_check_plaintext_equals_hash_salt_from_hash():
    assert bcrypt_check_plaintext_equals_hash("password", PASSWORD_HASH) is True
