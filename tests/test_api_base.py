from abc import ABC, abstractmethod
import pytest
from src.api_base import BaseAPI

def test_base_api_is_abstract():
    with pytest.raises(TypeError):
        BaseAPI()

def test_base_api_has_required_methods():
    assert hasattr(BaseAPI, "get")
    assert getattr(BaseAPI, "get").__isabstractmethod__
    assert hasattr(BaseAPI, "post")
    assert getattr(BaseAPI, "post").__isabstractmethod__
