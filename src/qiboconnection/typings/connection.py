from typing import TypedDict


class ConnectionConfiguration(TypedDict):
    user_id: int
    username: str
    api_key: str


class ConnectionEstablished(ConnectionConfiguration):
    authorisation_access_token: str
    api_path: str
