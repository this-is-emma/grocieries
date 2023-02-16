from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from grocery_app import db
from grocery_app.utils import FormEnum

class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'

class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

    def __str__(self):
        return self.title

class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(URLType)
    store_id = db.Column(db.Integer, db.ForeignKey('grocery_store.id'), nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    user_who_added_in_list = db.relationship('User', secondary = 'user_list', back_populates='shopping_list_items')

#User class for auth 
class User(UserMixin, db.Model):
    """user model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    shopping_list_items = db.relationship('GroceryItem', secondary = 'user_list', back_populates='user_who_added_in_list')


shopping_list_table = db.Table('user_list',
    Column('user_id', Integer, ForeignKey(User.id), primary_key=False),
    Column('groceryitem_id', Integer, ForeignKey(GroceryItem.id), primary_key=False),
    # db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    # db.Column('groceryitem_id', db.Integer, db.ForeignKey('groceryitem.id'))
)