import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
import json
from typing import Any
from qiboconnection.typings.connection import ConnectionEstablished

QIBO_CONFIG_DIR = "qibo_configuration"
QIBO_CONFIG_FILE = ".user_configuration.json"


def base64url_encode(payload) -> str:
    if isinstance(payload, dict):
        payload = json.dumps(payload)
    if not isinstance(payload, bytes):
        payload = payload.encode("utf-8")
    return urlsafe_b64encode(payload).decode("utf-8")


def base64url_decode(encoded_data: str) -> Any:
    return json.loads(urlsafe_b64decode(encoded_data).decode("utf-8"))


def write_config_file_to_disk(config_data: ConnectionEstablished) -> None:
    current_dir = os.getcwd()
    os.chdir(current_dir)
    if not os.path.isdir(QIBO_CONFIG_DIR):
        os.mkdir(QIBO_CONFIG_DIR)
    os.chdir(QIBO_CONFIG_DIR)

    with open(QIBO_CONFIG_FILE, "w") as config_file:
        json.dump(obj=config_data, fp=config_file, indent=2)
    os.chdir("..")


def load_config_file_to_disk() -> ConnectionEstablished:
    current_dir = os.getcwd()
    os.chdir(current_dir)
    os.chdir(QIBO_CONFIG_DIR)
    with open(QIBO_CONFIG_FILE) as config_file:
        os.chdir("..")
        return json.load(fp=config_file)
