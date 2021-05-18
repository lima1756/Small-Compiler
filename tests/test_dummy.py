from pytest import raises


class TestDummy:
    def test_dummy1(self):
        assert 1 == 1

    def test_dummy2(self):
        with raises(Exception):
            raise Exception("test")
