from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, SubmitField


class AssignCustomCategory(FlaskForm):
    transaction_id = HiddenField()
    category = SelectField("Category", choices=None, default=None)
    submit = SubmitField("Submit")
