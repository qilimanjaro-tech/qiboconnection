""" Tests methods for API platform settings calls """


from qiboconnection.api import API


def test_create_platform_settings(mocked_api: API):
    """Tests methods for platform settings"""
    assert isinstance(mocked_api, API)
    # platform = mocked_api.create_platform_settings()
    # assert isinstance(platform, dict)
