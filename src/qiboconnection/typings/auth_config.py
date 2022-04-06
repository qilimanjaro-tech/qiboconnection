""" Authentication Configuration Typing """
import enum
from dataclasses import dataclass
from typing import Literal


class UserRole(enum.Enum):
    """User Roles

    Args:
        enum (str): Available types of user roles:
        * user
        * admin
    """

    USER = "user"
    ADMIN = "admin"


class GrantType(enum.Enum):
    """Grant Type

    Args:
        enum (str): the only available grant type is urn:ietf:params:oauth:grant-type:jwt-bearer
    """

    JWT_BEARER = "urn:ietf:params:oauth:grant-type:jwt-bearer"


class UserScope(enum.Enum):
    """User Scope

    Args:
        enum (str): the only available scope is 'user profile'
    """

    USER = "user profile"


@dataclass
class AuthorisationRequestPayload:
    """Authorisation Request Payload

    Attributes:
        grantType (str): the grant type
        assertion (str): assertion
        scope (UserScope): User scope

    """

    grantType: Literal[GrantType.JWT_BEARER]  # pylint: disable=invalid-name
    assertion: str
    scope: UserScope


class TokenType(enum.Enum):
    """Token Type

    Args:
        enum (str): only available token type is 'bearer'
    """

    BEARER = "bearer"


@dataclass
class AccessTokenPartialPayload:
    """Access Token Partial Payload

    Attributes:
        user_id (int): the user id
        user_role (UserRole): user role
        aud: target audience of the token
    """

    user_id: int
    user_role: UserRole
    aud: str


@dataclass
class AccessTokenResponse:
    """Access Token Response

    Attributes:
        accessToken (str): the access token
        tokenType (str): the token type
        expiresIn (int): timestamp when the token expires
        issuedAt (str): string representation of the timestamp when token was issued
    """

    accessToken: str  # pylint: disable=invalid-name
    tokenType: Literal[TokenType.BEARER]  # pylint: disable=invalid-name
    expiresIn: int  # pylint: disable=invalid-name
    issuedAt: str  # pylint: disable=invalid-name


@dataclass
class AssertionPayload:
    """Assertion Payload

    Attributes:
        user_id (int): the user id
        username (str): the user name
        api_key (str): the api key associated to the user
        audience (str): target audience where token is used
        iat (int): timestamp when token was issued
    """

    user_id: int
    username: str
    api_key: str
    audience: str
    iat: int
