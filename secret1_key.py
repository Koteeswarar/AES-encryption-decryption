from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64


def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()


def encrypt_message(message):
    key = load_key()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()

    encryptor = cipher.encryptor()
    encrypted_bytes = encryptor.update(padded_message) + encryptor.finalize()

    return base64.b64encode(iv + encrypted_bytes).decode()


def decrypt_message(encrypted_data):
    key = load_key()
    encrypted_bytes = base64.b64decode(encrypted_data)

    iv = encrypted_bytes[:16]
    encrypted_message = encrypted_bytes[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_message = decryptor.update(encrypted_message) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(decrypted_padded_message) + unpadder.finalize()


message = input("Enter a Message:")
encrypted_msg = encrypt_message(message)
print("🔒 Encrypted:", encrypted_msg)

decrypted_msg = decrypt_message(encrypted_msg)
print("🔓 Decrypted:", decrypted_msg.decode())
