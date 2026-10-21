import stormpy


class TestSettings:
    def test_log_level(self):
        previous = stormpy.developer.get_log_level()
        try:
            stormpy.developer.set_log_level(stormpy.developer.LogLevel.DEBUG)
            assert stormpy.developer.get_log_level() == stormpy.developer.LogLevel.DEBUG
        finally:
            stormpy.developer.set_log_level(previous)

    def test_timeout(self):
        stormpy.developer.set_timeout_alarm(1000)
        stormpy.developer.reset_timeout_alarm()
