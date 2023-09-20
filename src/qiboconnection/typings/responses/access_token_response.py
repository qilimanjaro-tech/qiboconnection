""" AccessTokenRequest typing"""
from dataclasses import dataclass
from typing import Literal

from qiboconnection.typings.enums import TokenType


@dataclass
class AccessTokenResponse:
    """Access Token Response

    Attributes:
        accessToken (str): the access token
        accessToken (str): the refresh token
        tokenType (str): the token type
        expiresIn (int): timestamp when the token expires
        issuedAt (str): string representation of the timestamp when token was issued
    """

    accessToken: str  # pylint: disable=invalid-name
    refreshToken: str | None  # pylint: disable=invalid-name
    tokenType: Literal[TokenType.BEARER]  # pylint: disable=invalid-name
    expiresIn: int  # pylint: disable=invalid-name
    issuedAt: str  # pylint: disable=invalid-name
