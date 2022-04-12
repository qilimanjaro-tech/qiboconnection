""" Platform Schema related decorator functions """

from functools import wraps

from qiboconnection.models.platform_schema import PlatformSchema


def check_platform_schema_exists(fun):
    """Decorated function of check_platform_exists from Platform Schema
        that checks if the platform exists

    Raises:
        ValueError: platform_schema_id must be specified
        ValueError: when platform_schema_id is not found
    """

    @wraps(fun)
    def decorated(*args, **kwargs):
        if "platform_schema_id" not in kwargs:
            raise ValueError("platform_schema_id must be specified")
        platform_schema_id = kwargs["platform_schema_id"]
        PlatformSchema().check_platform_schema_exists(platform_schema_id=platform_schema_id)
        return fun(*args, **kwargs)

    return decorated
