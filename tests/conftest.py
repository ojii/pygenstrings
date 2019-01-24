import shutil

import pytest
from _pytest.nodes import Node


def pytest_itemcollected(item: Node):
    if not shutil.which("genstrings"):
        item.add_marker(pytest.mark.skip("genstrings not found"))
