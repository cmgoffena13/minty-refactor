from minty.templates.filters import (
    format_boolean,
    format_currency,
    good_accuracy,
    limit_characters,
)

jinja_filters = []

jinja_filters.append(format_boolean)
jinja_filters.append(format_currency)
jinja_filters.append(good_accuracy)
jinja_filters.append(limit_characters)
