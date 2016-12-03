from flask_wtf import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class ZipSearchForm(Form):
    zip = IntegerField('city_search', validators=[DataRequired(), NumberRange(min=0, max=100000,
                                                                              message='Please enter a valid zip code')])

