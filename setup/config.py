import configparser
import os
import multiprocessing


class SetupConfig:
    """
    Configuration for setup.
    """

    def __init__(self):
        """
        Create config with default values
        """
        self.config = configparser.ConfigParser()
        self.config["build_ext"] = self._default_values()

    @staticmethod
    def _default_values():
        """
        Return default values for config.

        :return: Dict with default values for build settings.
        """
        try:
            no_jobs = multiprocessing.cpu_count() if multiprocessing.cpu_count() is not None else 1
        except NotImplementedError:
            no_jobs = 1
        return {
            "storm_dir": "",
            "disable_dft": False,
            "disable_gspn": False,
            "disable_pars": False,
            "disable_pomdp": False,
            "carl_dir": "",
            "carl_parser_dir": "",
            "disable_cln": False,
            "disable_parser": False,
            "debug": False,
            "jobs": str(no_jobs),
            "pybind_version": "",
        }

    def load_from_file(self, path):
        """
        Load config from file.
        :param path Path to config file.
        """
        if os.path.isfile(path):
            self.config.read(path)
            if not self.config.has_section("build_ext"):
                self.config["build_ext"] = self._default_values()

    def write_config(self, path):
        """
        Save config with build settings.
        :param path Path to config file.
        """
        with open(path, 'w') as configfile:
            self.config.write(configfile)

    def get_as_bool(self, name):
        """
        Get the boolean value for option name.
        :param name: Name of option.

        :return Value as bool.
        """
        return self.config.getboolean("build_ext", name)

    def get_as_int(self, name):
        """
        Get the int value for option name.
        :param name: Name of option.

        :return Value as integer.
        """
        return self.config.getint("build_ext", name)

    def get_as_string(self, name):
        """
        Get the string value for option name.
        :param name: Name of option.

        :return Value as string.
        """
        return self.config.get("build_ext", name)

    def update(self, name, value):
        """
        Update name with given value if value is not None.
        :param name: Name of option.
        :param value: New value or None
        """
        if value is not None:
            assert self.config.has_option("build_ext", name)
            self.config.set("build_ext", name, str(value))
