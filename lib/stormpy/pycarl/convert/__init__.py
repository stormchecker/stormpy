from . import gmp_converter

from stormpy.pycarl._config import CARL_WITH_CLN as has_cln


def convert_to_gmp(data):
    """
    Convert data type to gmp.
    :param data: data structure.
    :return: gmp data structure.
    """
    return gmp_converter.convert(data)


if has_cln:
    from . import cln_converter

    def convert_to_cln(data):
        """
        Convert data type to cln.
        :param data: data structure.
        :return: cln data structure.
        """
        return cln_converter.convert(data)
