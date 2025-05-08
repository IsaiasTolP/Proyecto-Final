from cryptography.fernet import Fernet
import os

KEY_PATH = 'secret.key'

def generate_key():
    """
    Generate a key for encryption and decryption.
    """
    key = Fernet.generate_key()
    with open(KEY_PATH, 'wb') as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_PATH):
        generate_key()
    with open('secret.key', 'rb') as key_file:
        return Fernet(key_file.read())
    
fernet = load_key()