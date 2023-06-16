from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField


class DeleteModel(FlaskForm):
    classifier_name = HiddenField()
    submit = SubmitField("X")
