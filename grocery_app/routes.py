from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    # TODO: Create a GroceryStoreForm

    # TODO: If form was submitted and was valid:
    # - create a new GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.

    form = GroceryStoreForm()
    if form.validate_on_submit():
        new_store = GroceryStore (
            title = form.title.data, 
            address = form.address.data
        )
            
        db.session.add(new_store)
        db.session.commit()
        flash('New store was created successfully.')
        return redirect(url_for('main.homepage'))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form = form)

@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    # TODO: Create a GroceryItemForm
    form = GroceryItemForm()
    # TODO: If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        new_item = GroceryItem(
            name = form.name.data,
            price = form.price.data,
            category = form.category.data,
            photo_url = form.photo_url.data,
            store = form.store.data
        )

        db.session.add(new_item)
        db.session.commit()
        flash('New item was created successfully.')
        return redirect(url_for('main.item_detail', item_id=new_item.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form = form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)
    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    if form.validate_on_submit():        
        store = GroceryStore.query.get(store_id)
        new_title = form.title.data
        new_address = form.address.data 

        store.title = new_title
        store.address = new_address
        db.session.commit()
        
        # TODO: Send the form to the template and use it to render the form fields
        flash('Store updated successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # TODO: Create a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj=item)
    # TODO: If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        item = GroceryItem.query.get(item_id)
        new_name = form.name.data
        new_price = form.price.data
        new_category = form.category.data
        new_photo_url = form.photo_url.data
        new_store_id = form.store.data
        item.name = new_name
        item.price = new_price
        item.category = new_category
        item.photo_url = new_photo_url
        item.store_id = new_store_id.id
        # TODO: Send the form to the template and use it to render the form fields
        db.session.commit()
        flash('Item updated successfully.')
        return redirect(url_for('main.item_detail', item_id=item.id))
    print(form.errors)
    return render_template('item_detail.html', item=item, form=form)


