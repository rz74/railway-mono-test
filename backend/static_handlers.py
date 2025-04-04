import os
from flask import send_file, jsonify
from werkzeug.exceptions import NotFound

# Default secrets path — can later be moved to path_config
SECRETS_DIR = os.environ.get("PUZZLE_SECRETS_DIR", "./backend/secrets")


def _secure_serve_file(filename: str, mime_type: str):
    path = os.path.join(SECRETS_DIR, filename)
    if not os.path.exists(path):
        print(f"❌ Missing secret file: {filename}")
        raise NotFound(description=f"{filename} not found in secrets directory.")
    print(f"📤 Serving secret: {filename}")
    return send_file(path, mimetype=mime_type)


def serve_key():
    return _secure_serve_file("key.txt", "text/plain")


def serve_index_map():
    return _secure_serve_file("index-map.json", "application/json")


def serve_obfuscation_map():
    return _secure_serve_file("obfuscation-map.json", "application/json")


def serve_target():
    return _secure_serve_file("target.txt", "text/plain")


def serve_mode():
    return _secure_serve_file("delivery-mode.txt", "text/plain")
