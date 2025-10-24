from ._info import *
from . import _config


def storm_version() -> str:
    """
    Get Storm version.

    :return: Storm version
    :rtype: str
    """
    return _config.STORM_VERSION


def storm_from_system() -> bool:
    """
    Does stormpy rely on a (pre-existing) system installation of Storm.
    System versions include anything on the system
    that was not fetched during the build of stormpy.

    :return: True, if stormpy linked against a preexisting Storm installation.
    """
    return _config.STORM_FROM_SYSTEM


def storm_development_version() -> bool:
    """
    Is true, if the version of Storm was marked as modified since release.

    :return: True if a development version
    """
    return _config.STORM_DEVELOPER_VERSION


def storm_origin_info() -> [str | None, str | None]:
    """
    Information about the source of Storm, in particular the repo path and the repo tag.

    If Storm was already on the system during installation and this preexisting version was used,
    these values are expected to be ``None``.
    If Storm was installed (locally) as part of the installation process, these values are expected to be not ``None``.
    Then:

    - The repo path usually takes the form of a url
    - The tag refers to a tag on the repo.

    A noteworthy exception is when the fetch was from a local source dir.
    In that case, this source dir is included, and the tag reads ``__local-source-dir__``.

    :return: A pair with the repo path and the repo tag.
    """
    return (_config.STORM_ORIGIN_REPO, _config.STORM_ORIGIN_TAG)


def storm_directory() -> str | None:
    """
    Return the Storm directory which is used by stormpy.

    If a prexisting installation of Storm was used, then the path to this directory is returned.
    If Storm was installed during the installation process, value ``None`` is returned.

    :return: Storm directory.
    """
    return _config.STORM_DIRECTORY


def storm_exact_use_cln() -> bool:
    """
    Check if exact arithmetic in Storm uses CLN or GMP.

    :return: True iff exact arithmetic uses CLN.
    :rtype: bool
    """
    return _config.STORM_CLN_EA


def storm_ratfunc_use_cln() -> bool:
    """
    Check if rational functions in Storm use CLN or GMP.

    :return: True iff rational functions use CLN.
    :rtype: bool
    """
    return _config.STORM_CLN_RF
