from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, SubmitField


class ActiveModel(FlaskForm):
    classifier_name = HiddenField()
    active = SelectField("Active", choices=(True, False), default=None)
    submit = SubmitField("Submit")
