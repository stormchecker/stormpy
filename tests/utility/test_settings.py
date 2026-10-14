import stormpy


class TestSettings:
    def test_log_level(self):
        previous = stormpy.developer.get_log_level()
        stormpy.utility.set_log_level(stormpy.utility.LogLevel.DEBUG)
        assert stormpy.developer.get_log_level() == stormpy.utility.LogLevel.DEBUG
        stormpy.utility.set_log_level(previous)

    def test_timeout(self):
        stormpy.utility.set_timeout(1000)
        stormpy.utility.reset_timeout()
