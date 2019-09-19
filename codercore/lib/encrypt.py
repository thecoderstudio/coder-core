import bcrypt


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
