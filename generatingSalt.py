import hashlib
import os
import sqlite3


def generatePassword(password):
    salt = os.urandom(32)

    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,
        dklen=128  # 128 byte key
    )

    storage = salt + key
    return storage









