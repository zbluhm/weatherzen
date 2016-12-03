from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class CitySearchForm(Form):
    city = StringField('city_search', validators=[DataRequired()])

