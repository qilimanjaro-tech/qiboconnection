"""Users web responses module"""

users_base_response_without_slack_id = {
    "user_id": 0,
    "username": "remote_username",
}

users_base_response = {
    **users_base_response_without_slack_id,
    "slack_id": "remote_slack_id",
}


class Users:
    """Users Web Responses"""

    retrieve_response: tuple[dict, int] = (users_base_response, 200)
    retrieve_response_without_slack_id: tuple[dict, int] = (users_base_response_without_slack_id, 200)
    ise_response: tuple[dict, int] = ({}, 500)
    update_response: tuple[dict, int] = retrieve_response
