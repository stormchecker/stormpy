"""Value-type conversion for schedulers."""

from __future__ import annotations

from stormpy.developer import storage
from . import Scheduler


def _to_value_type(self: Scheduler, value_type: type = float) -> Scheduler:
    """Convert a scheduler's choice probabilities to another value type.

    :param value_type: Target numeric type, such as float or stormpy.Rational.
    :return: A new scheduler using the requested numeric type.
    :raises TypeError: If conversion between the selected types is unsupported.
    """
    return storage.to_value_type[value_type](self)


for _class in storage.Scheduler.instantiations.values():
    _class.to_value_type = _to_value_type
