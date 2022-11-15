import pytest
import new_main_noop as m


def test_split():
    assert m.split(["5", "5"], ["7"]) == (["5"], ["5"])