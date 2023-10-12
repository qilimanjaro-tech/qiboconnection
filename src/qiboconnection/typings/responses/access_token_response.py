# Copyright 2023 Qilimanjaro Quantum Tech
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
