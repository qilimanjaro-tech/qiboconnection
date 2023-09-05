""" Authentication Configuration Typing """
from dataclasses import dataclass

# @dataclass
# class AuthorisationRequestPayload:
#     """Authorisation Request Payload
#
#     Attributes:
#         grantType (str): the grant type
#         assertion (str): assertion
#         scope (UserScope): User scope
#
#     """
#
#     grantType: Literal[GrantType.JWT_BEARER]  # pylint: disable=invalid-name
#     assertion: str
#     scope: UserScope
#
#
# @dataclass
# class AccessTokenPartialPayload:
#     """Access Token Partial Payload
#
#     Attributes:
#         user_id (int): the user id
#         user_role (UserRole): user role
#         aud: target audience of the token
#     """
#
#     user_id: int
#     user_role: UserRole
#     aud: str


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
