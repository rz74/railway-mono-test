import os

# Root path of the backend (this file's grandparent)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === Template site directory ===
TEMPLATE_SITE_DIR = os.path.join(BASE_DIR, "template_site")

# === Runtime secrets directory (used by Flask routes) ===
SECRETS_DIR = os.path.join(BASE_DIR, "secrets")

# === Static asset paths ===
FAVICON_PATH = os.path.join(BASE_DIR, "static", "favicon.ico")

# === Filenames for secrets ===
KEY_FILE = "key.txt"
INDEX_MAP_FILE = "index-map.json"
OBFUSCATION_MAP_FILE = "obfuscation-map.json"
TARGET_FILE = "target.txt"
MODE_FILE = "delivery-mode.txt"

# === Helper for full secret file path ===
def secret_path(filename: str) -> str:
    return os.path.join(SECRETS_DIR, filename)

# === Static directory ===
STATIC_DIR = os.path.join(BASE_DIR, "static")
