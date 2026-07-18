import os
from cryptography.fernet import Fernet
from pathlib import Path
from dotenv import load_dotenv

env_path = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)

# In a local desktop app, if the key is missing, we auto-generate and persist it.
SECRET_KEY = os.environ.get("BrainWeb_SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = Fernet.generate_key().decode('utf-8')
    os.environ["BrainWeb_SECRET_KEY"] = SECRET_KEY
    try:
        with open(env_path, "a") as f:
            f.write(f"\nBrainWeb_SECRET_KEY={SECRET_KEY}\n")
    except Exception as e:
        print(f"Warning: Could not save SECRET_KEY to {env_path}: {e}")

fernet = Fernet(SECRET_KEY.encode('utf-8'))

def encrypt_api_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode('utf-8')).decode('utf-8')

def decrypt_api_key(encrypted_key: str) -> str:
    return fernet.decrypt(encrypted_key.encode('utf-8')).decode('utf-8')

def mask_api_key(api_key: str) -> str:
    if len(api_key) <= 8:
        return "***"
    return f"{api_key[:3]}...{api_key[-4:]}"
