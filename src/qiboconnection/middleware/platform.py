""" Platform related decorator functions """

from functools import wraps

from qiboconnection.models.platform import Platform


def check_platform_exists(fun):
    """Decorated function of check_platform_exists from Platform
        that checks if the platform exists

    Raises:
        ValueError: platform_id must be specified
        ValueError: when platform_id is not found
    """

    @wraps(fun)
    def decorated(*args, **kwargs):
        if "platform_id" not in kwargs:
            raise ValueError("platform_id must be specified")
        platform_id = kwargs["platform_id"]
        Platform().check_platform_exists(platform_id=platform_id)
        return fun(*args, **kwargs)

    return decorated
