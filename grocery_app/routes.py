from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, LoginForm, SignUpForm
from grocery_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)



@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
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
            address = form.address.data,
            created_by_id = current_user.id
        )
            
        db.session.add(new_store)
        db.session.commit()
        flash('New store was created successfully.')
        return redirect(url_for('main.homepage'))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form = form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
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
            store = form.store.data,
            created_by_id = current_user.id
        )
        this_item = db.session.merge(new_item)
        db.session.add(this_item)
        db.session.commit()
        flash('New item was created successfully.')
        return redirect(url_for('main.item_detail', item_id=this_item.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form = form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)
    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    if form.validate_on_submit(): 
        print('went in the loop!')       
        store = GroceryStore.query.get(store_id)
        new_title = form.title.data
        new_address = form.address.data 
        store.title = new_title
        store.address = new_address
        db.session.merge(store)
        db.session.commit()
        
        # TODO: Send the form to the template and use it to render the form fields
        flash('Store updated successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))
    print(f'Form errors: {form.errors}')
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
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
        db.session.merge(item)
        db.session.commit()
        flash('Item updated successfully.')
        return redirect(url_for('main.item_detail', item_id=item.id))
    return render_template('item_detail.html', item=item, form=form)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    # ... adds item to current_user's shopping list
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item) 
    print(current_user.shopping_list_items)
    # TODO: If the book is not already in user's favorites, then add it,
    # commit the change to the database, and flash a success message.
    if item not in current_user.shopping_list_items:
        print('Went it the loop!')
        current_user.shopping_list_items.append(item)
        db.session.merge(current_user)
        db.session.commit()
        print(current_user.shopping_list_items)
        flash('Item added to shopping list...')
        return redirect(url_for('main.item_detail', item_id=item.id))
    else:
        flash('Item already in your list')
        print('item already in the list...')
    return render_template('item_detail.html', item=item, form=form)


@main.route('/shopping_list', methods=['GET'])
@login_required
def shopping_list():
    print('Im in the shopping list route..')
    # ... get logged in user's shopping list items ...
    print(current_user.shopping_list_items)
    list = current_user.shopping_list_items
    print(list)
    # ... display shopping list items in a template ...
    return render_template('shopping_list.html', list=list)

# routes.py
auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
