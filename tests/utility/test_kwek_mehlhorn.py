import stormpy
import stormpy.utility


class TestKwekMehlhorn:
    def test_sharpen_exact(self):
        rational = stormpy.utility.sharpen(5, 0.5)
        assert rational == stormpy.Rational("1/2")

    def test_sharpen_approximation(self):
        rational = stormpy.utility.sharpen(10, 1 / 3)
        assert abs(float(rational) - 1 / 3) < 0.01

    def test_sharpen_zero(self):
        rational = stormpy.utility.sharpen(5, 0.0)
        assert rational == stormpy.Rational("0")

    def test_sharpen_one(self):
        rational = stormpy.utility.sharpen(5, 1.0)
        assert rational == stormpy.Rational("1")
