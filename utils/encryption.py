from cryptography.fernet import Fernet

# Permanent encryption key
key = b'JxeIhFis7u_0fKfcCMeUjAmBt8LfEcKTAVdITknFyU8='

cipher = Fernet(key)

def encrypt_data(data):
    return cipher.encrypt(data.encode())

def decrypt_data(data):
    return cipher.decrypt(data).decode()