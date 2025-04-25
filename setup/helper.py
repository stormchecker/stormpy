import importlib
import os
import re
import sys


def ensure_dir_exists(path):
    """
    Check whether the directory exists and creates it if not.
    """
    assert path is not None
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise IOError("Cannot create directory: " + path)
    except BaseException:
        raise IOError("Path " + path + " seems not valid")


def parse_storm_version(version_string):
    """
    Parses the version of storm.

    :param version_string: String containing version information.
    :return: Tuple (version, commit)
    """
    split = version_string.split("-")
    version = split[0]
    commit = ""
    if len(split) > 1:
        commit = split[1]
    return version, commit


def parse_carl_version(version_string):
    """
    Parses the version of carl.

    :param version_string: String containing version information.
    :return: Tuple (version, commit)
    """
    split = version_string.split("-")
    version = split[0]
    commit = ""
    if len(split) > 1:
        commit = split[1]
    return version, commit


def obtain_version():
    """
    Obtains the version as specified in stormpy.

    :return: Version
    """
    verstr = "unknown"
    try:
        verstrline = open("lib/stormpy/_version.py", "rt").read()
    except EnvironmentError:
        pass  # Okay, there is no version file.
    else:
        VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
        mo = re.search(VSRE, verstrline, re.M)
        if mo:
            verstr = mo.group(1)
        else:
            raise RuntimeError("unable to find version in stormpy/_version.py")
    return verstr


def load_cmake_config(path):
    """
    Load cmake config.
    :param path: Path.
    :return: Configuration.
    """
    if sys.version_info[1] >= 5:
        # Method for Python >= 3.5
        spec = importlib.util.spec_from_file_location("genconfig", path)
        conf = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(conf)
        return conf
    else:
        # Deprecated method for Python <= 3.4
        from importlib.machinery import SourceFileLoader

        return SourceFileLoader("genconfig", path).load_module()
