from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField
from wtforms.validators import DataRequired


class CreateNewModel(FlaskForm):
    classifier_name = StringField("Model Name", validators=[DataRequired()])
    date_filter = DateField("Date Filter", validators=[DataRequired()])
    submit = SubmitField("Submit")
