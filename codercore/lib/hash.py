import bcrypt

EXPECTED_SALT_LENGTH = 29
ENCODING = "utf-8"


def bcrypt_hash(plaintext: str, salt: bytes | None = None) -> tuple[str, str]:
    """Hash a plaintext string with bcrypt, returning (hash, salt) as strings."""
    if not salt:
        salt = bcrypt.gensalt()

    return (
        bcrypt.hashpw(plaintext.encode(ENCODING), salt).decode(ENCODING),
        salt.decode(ENCODING),
    )


def bcrypt_check_plaintext_equals_hash(
    plaintext: str, hashed_plaintext: str, salt: str | None = None
) -> bool:
    """Verify that a plaintext string matches a bcrypt hash string."""
    if not salt:
        salt = hashed_plaintext[:EXPECTED_SALT_LENGTH]

    new_hashed_plaintext = bcrypt.hashpw(
        plaintext.encode(ENCODING), salt.encode(ENCODING)
    )
    return new_hashed_plaintext == hashed_plaintext.encode(ENCODING)
