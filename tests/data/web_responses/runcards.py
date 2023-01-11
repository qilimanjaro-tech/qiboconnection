""" Runcards Web Responses """


class Runcards:
    """Runcards Web Responses"""

    create_response: tuple[dict, int] = ({}, 201)

    retrieve_many_response: tuple[dict, int] = ({}, 200)

    retrieve_response: tuple[dict, int] = ({}, 200)

    update_response: tuple[dict, int] = ({}, 200)

    delete_response: tuple[dict, int] = ({}, 204)
