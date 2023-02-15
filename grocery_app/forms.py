
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL

from grocery_app.models import GroceryStore, ItemCategory

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    # TODO: Add the following fields to the form class:
    # - title - StringField
    # - address - StringField
    # - submit button
    title = StringField('Title:', 
        validators=[
            DataRequired(), 
            Length(min=3, max=80, message="title must be between 3 and 80 chars")
        ]) 
    address = StringField('address:', 
        validators=[
            DataRequired(), 
            Length(min=3, max=80, message="address needs to be betweeen 3 and 80 chars")
        ])

    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField('Name:', 
        validators=[
            DataRequired(), 
            Length(min=3, max=80, message="Name must be between 3 and 80 chars")
        ]) 
    price = FloatField('price')
    category = SelectField('Category', choices=ItemCategory.choices())
    photo_url = StringField(
        'Photo:', 
        validators=[
            DataRequired(), 
            Length(min=3, max=80, message="photo needs to be a valid url")
        ]
    )
    store = QuerySelectField('Grocery store', query_factory=lambda: GroceryStore.query, allow_blank=False)

    #submit
    submit = SubmitField('Submit')
    
