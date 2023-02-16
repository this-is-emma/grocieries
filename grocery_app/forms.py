from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from wtforms import StringField, PasswordField, SubmitField
from grocery_app.extensions import bcrypt
from grocery_app.models import User

from grocery_app.models import GroceryStore, ItemCategory

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
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

#AUTH FORMS

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')
    
