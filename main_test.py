import pytest
import main as m


def test_create_shoe():
    assert len(m.create_shoe(0)) == 0


