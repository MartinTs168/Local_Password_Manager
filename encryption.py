from os.path import exists
from cryptography.fernet import Fernet


def generate_encryption_key():

    if not exists("key.key"):
        with open("key.key", "wb") as f:
            key = Fernet.generate_key()
            f.write(key)


def get_key():
    with open("key.key", "rb") as f:
        key = f.read()

    return key


def encrypt(string: str):
    fernet_key = Fernet(get_key())

    encrypted_string = fernet_key.encrypt(string.encode())

    return encrypted_string


def decrypt(string: str):
    ferenet_key = Fernet(get_key())

    decrypted_string = ferenet_key.decrypt(string).decode()

    return decrypted_string
