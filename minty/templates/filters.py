from decimal import Decimal
from numbers import Number

from markupsafe import Markup


def format_currency(value):
    if not isinstance(value, (Number, Decimal)):
        raise TypeError("Value must be Number.")
    if value < 0:
        return Markup('<span style="color:red">-<span>' + format_currency(-value))
    return "${:,.2f}".format(value)


def limit_characters(value, length=30):
    _value = None
    if not isinstance(value, str):
        raise TypeError("Value must be a string")
    if len(value) > length:
        index_v = length - 1
        _value = value[:index_v] + "..."
    else:
        _value = value
    return _value


def good_accuracy(value):
    if not isinstance(value, (Number, Decimal)) and value is not None:
        raise TypeError("Value must be Number.")
    if value is None:
        _value = None
        return _value
    if value < 0.70:
        _value = Markup('<span style="color:red;">' + str(value) + "</span>")
    if value > 0.90:
        _value = Markup('<span style="color:green;">' + str(value) + "</span>")
    if value > 0.70 and value < 0.90:
        _value = Markup('<span style="color:orange;">' + str(value) + "</span>")
    return _value
