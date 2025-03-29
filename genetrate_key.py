import os


key = os.urandom(32)

with open("secret.key", "wb") as key_file:
    key_file.write(key)

print("✅ Secret key saved to 'secret.key'")
