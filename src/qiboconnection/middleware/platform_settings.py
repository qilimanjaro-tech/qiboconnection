""" Platform related decorator functions """

from functools import wraps

from qiboconnection.models.platform_settings import PlatformSettings


def check_platform_settings_exists(fun):
    """Decorated function of check_platform_settings_exists from Platform
        that checks if the platform settings exists

    Raises:
        ValueError: platform_id must be specified
        ValueError: when platform_id is not found
    """

    @wraps(fun)
    def decorated(*args, **kwargs):
        if "platform_schema_id" not in kwargs:
            raise ValueError("platform_schema_id must be specified")
        platform_schema_id = kwargs["platform_schema_id"]
        if "platform_settings_id" not in kwargs:
            raise ValueError("platform_settings_id must be specified")
        platform_settings_id = kwargs["platform_settings_id"]
        PlatformSettings().check_platform_settings_exists(
            platform_schema_id=platform_schema_id, platform_settings_id=platform_settings_id
        )
        return fun(*args, **kwargs)

    return decorated
