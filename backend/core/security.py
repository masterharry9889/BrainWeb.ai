import os
from cryptography.fernet import Fernet

# In a real app, this MUST come from an environment variable and never be committed.
# For local v1 development, we use a fixed mock key so restarts don't invalidate DB keys.
SECRET_KEY = os.environ.get("INGOT_SECRET_KEY", "uO6_M2Jt4eW-PzHhIuU3C05iWw-C5K8V7h8J9sU4z6E=")

fernet = Fernet(SECRET_KEY.encode('utf-8'))

def encrypt_api_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode('utf-8')).decode('utf-8')

def decrypt_api_key(encrypted_key: str) -> str:
    return fernet.decrypt(encrypted_key.encode('utf-8')).decode('utf-8')

def mask_api_key(api_key: str) -> str:
    if len(api_key) <= 8:
        return "***"
    return f"{api_key[:3]}...{api_key[-4:]}"
