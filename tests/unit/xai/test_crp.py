"""CRP lens tests.
"""

from lczerolens.xai import CrpLens


class TestLens:
    def test_is_compatible(self, tiny_wrapper):
        lens = CrpLens()
        assert lens.is_compatible(tiny_wrapper)