import os
from cryptography.fernet import Fernet

# Generate a new key if it doesn't exist
if not os.path.exists('encryption_key.txt'):
    key = Fernet.generate_key()
    with open('encryption_key.txt', 'wb') as key_file:
        key_file.write(key)
else:
    with open('encryption_key.txt', 'rb') as key_file:
        key = key_file.read()

# Decode the key for use
ENCRYPTION_KEY = key.decode() 