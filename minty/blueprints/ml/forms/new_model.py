from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired


class CreateNewModel(FlaskForm):
    classifier_name = StringField("Model Name", validators=[DataRequired()])
    importance_threshold = DecimalField("Importance Threshold", default=0.0)
    date_filter = DateField("Date Filter", validators=[DataRequired()])
    submit = SubmitField("Submit")
