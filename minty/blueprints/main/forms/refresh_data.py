from flask_wtf import FlaskForm
from mintapi.filters import DateFilter
from wtforms import SelectField, SubmitField

options = [member.name for member in DateFilter.Options if member.name != "CUSTOM"]


class RefreshData(FlaskForm):
    date_filter = SelectField("Date Filter", choices=options)
    submit = SubmitField("Refresh Data")
