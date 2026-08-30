# tests/test_storage_base.py
from abc import ABCMeta
import pytest
from src.storage_base import StorageBase

def test_storage_base_is_abstract():
    with pytest.raises(TypeError):
        StorageBase()
