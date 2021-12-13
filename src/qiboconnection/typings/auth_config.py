from typing import Literal, TypedDict
import enum


class UserRoles(enum.Enum):
    user = "user"
    admin = "admin"


class GrantType(enum.Enum):
    jwt_bearer = "urn:ietf:params:oauth:grant-type:jwt-bearer"


class UserScope(enum.Enum):
    user = "user profile"


class AuthorisationRequestPayload(TypedDict):
    grantType: Literal[GrantType.jwt_bearer]
    assertion: str
    scope: UserScope


class TokenType(enum.Enum):
    bearer = "bearer"


class AccessTokenPartialPayload(TypedDict):
    user_id: int
    user_role: UserRoles
    aud: str


class AccessTokenResponse(TypedDict):
    accessToken: str
    tokenType: Literal[TokenType.bearer]
    expiresIn: int
    issuedAt: str


class AssertionPayload(TypedDict):
    user_id: int
    username: str
    api_key: str
    audience: str
    iat: int
