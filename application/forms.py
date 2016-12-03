from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class ZipSearchForm(Form):
    zip = StringField('city_search', validators=[DataRequired()])

