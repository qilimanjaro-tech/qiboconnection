""" Users web responses module """

users_base_response = {
    "user_id": 0,
    "username": "remote_username",
    "slack_id": "remote_slack_id",
}


class Users:
    """Users Web Responses"""

    retrieve_response: tuple[dict, int] = (users_base_response, 200)
    ise_response: tuple[dict, int] = ({}, 500)
    update_response: tuple[dict, int] = retrieve_response
