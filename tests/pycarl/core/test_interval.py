from stormpy import pycarl
from configurations import PackageSelector


class TestIntervalDouble:
    def test_init(self):
        interval = pycarl.Interval(1)
        assert interval.isPointInterval
        assert interval.lower() == 1

    def test_addition(self):
        int1 = pycarl.Interval(2, 4)
        int2 = pycarl.Interval(-1, 1)
        res = int1 + int2
        assert res.lower() == 1
        assert res.upper() == 5


class TestInterval(PackageSelector):
    def test_init(self, package):
        interval = package.Interval(package.Rational(1))
        assert interval.isPointInterval
        assert interval.lower() == 1

    def test_addition(self, package):
        int1 = package.Interval(package.Rational(2), package.Rational(4))
        int2 = package.Interval(package.Rational(-1), package.Rational(1))
        res = int1 + int2
        assert res.lower() == 1
        assert res.upper() == 5
