import pytest

from qiboconnection.api import API


def test_api_constructor():
    """Test API class constructor"""
    api = API()
    assert isinstance(api, API)
