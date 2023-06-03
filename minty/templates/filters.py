from decimal import Decimal
from numbers import Number

from markupsafe import Markup


def format_currency(value):
    if not isinstance(value, (Number, Decimal)):
        raise TypeError("Value must be Number.")
    if value < 0:
        return Markup('<span style="color:red">-<span>' + format_currency(-value))
    return "${:,.2f}".format(value)


def limit_characters(value):
    _value = None
    if not isinstance(value, str):
        raise TypeError("Value must be a string")
    if len(value) > 60:
        _value = value[:59] + "..."
    else:
        _value = value
    return _value
