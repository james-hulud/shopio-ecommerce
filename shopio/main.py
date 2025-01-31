from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import QuantityForm, SearchForm, RemoveFromBasketForm, PaymentForm, AddressForm, RegistrationForm, LoginForm, EditAddressForm, EditPaymentDetailsForm
from databases import db, Products, User, Address, PaymentDetails
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.route('/', methods=['GET', 'POST'])
def galleryPage():
    items = Products.query.all()
    add_form = QuantityForm()
        
    if add_form.validate_on_submit():
        item = request.form.get('item_data')
        item_data = item.split(',')
        
        if f'quantity{item_data[0]}' not in session:
            print("New session", flush=True)
            session[f'quantity{item_data[0]}'] = 0
            
        session[f'quantity{item_data[0]}'] += int(add_form.quantity.data)
        
        if item_data not in session['basket']:
            session['basket'].append(item_data)
            
        return redirect(url_for('basketPage'))
    
    return render_template('index.html', items = items, add_form = add_form)

@app.route('/products/<int:itemId>', methods=['GET','POST'])
def singleProductPage(itemId):
    # Here itemId is primary key of document
    item = Products.query.get(itemId)
    print(item)
    
    add_form = QuantityForm()
    return render_template('single_item.html', item = item, add_form = add_form)

@app.route('/basket', methods=['GET','POST'])
def basketPage():
    
    if 'basket' not in session:
        print("New session", flush=True)
        session['basket'] = []
        
    remove_form = RemoveFromBasketForm()
    
    if remove_form.validate_on_submit():
        item_id = request.form.get('item_id')
        basket = session['basket']
        new_basket = []
        for item in basket:
            if item[0] == item_id:
                continue
            new_basket.append(item)
        
        session[f'quantity{item_id}'] = 0
        session['basket'] = new_basket
    
    return render_template('basket.html', basket = session['basket'], remove_form = remove_form)

@app.route('/signin', methods=['GET','POST'])
def signInPage():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user)
                return redirect(url_for('galleryPage'))
        
    return render_template('sign_in.html', sign_in_form = form)

@app.route('/signout', methods=['GET','POST'])
@login_required
def signOutUser():
    logout_user()
    return redirect(url_for('signInPage'))

@app.route('/<string:username>/account', methods=['GET','POST'])
@login_required
def dashboardPage(username):
    if current_user.is_authenticated:
        username = current_user.username
        return render_template('dashboard.html', username = username)


@app.route('/register', methods=['GET','POST'])
def registerPage():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        new_user = User(email=form.email.data, password=form.password.data, username=form.username.data)
        db.session.add(new_user)
        db.session.commit()
        print("New user created successfully")
        return redirect(url_for('signInPage'))
    
    return render_template('register.html', register_form = form)

@app.route('/results')
def searchResults(search):
    results = []
    search_string = search.data['search']
    
    if search.data['search'] == '':
        query = Products.query.all()
        results = query
    
    if not results:
        flash('No results found')
        return redirect(url_for('galleryPage'))
    else:
        return render_template('results.html', results = results)

@app.route('/checkout', methods=['GET', 'POST'])
def checkoutPage():
    payment_form = PaymentForm()
    address_form = AddressForm()
    edit_address_form = EditAddressForm()
    edit_payment_form = EditPaymentDetailsForm()
    
    # if user is logged in
    if current_user.is_authenticated:
        user_address = Address.query.filter_by(user_id=current_user.id).first()
        user_payment_details = PaymentDetails.query.filter_by(user_id=current_user.id).first()
        form_id = request.form.get('form_id')
        
        if address_form.validate_on_submit():
            user_address = Address(
                full_name=address_form.full_name.data,
                phone_number=address_form.phone_number.data,
                postcode=address_form.postcode.data,
                address_line_one = address_form.address_line_one.data,
                address_line_two = address_form.address_line_two.data,
                town_city=address_form.town_city.data,
                county=address_form.county.data,
                user_id=current_user.id,
                user_ad=current_user
            )
            db.session.add(user_address)
            db.session.commit()
            return redirect(url_for('checkoutPage'))
        
        elif payment_form.validate_on_submit():
            user_payment_details = PaymentDetails(
                name_on_card=payment_form.name_on_card.data,
                card_number=payment_form.card_number.data,
                expiry_date=payment_form.expiry_date.data,
                security_number=payment_form.security_number.data,
                user_id=current_user.id,
                user_pd=current_user
            )
            db.session.add(user_payment_details)
            db.session.commit()
            return redirect(url_for('checkoutPage'))
        
        elif edit_payment_form.validate_on_submit() and user_payment_details and form_id == 'edit_payment':
            db.session.delete(user_payment_details)
            db.session.commit()
            return redirect(url_for('checkoutPage'))
        
        elif edit_address_form.validate_on_submit() and user_address and form_id == 'edit_address':
            db.session.delete(user_address)
            db.session.commit()
            return redirect(url_for('checkoutPage'))
        
        return render_template('checkout.html', address_form = address_form, payment_form = payment_form, basket = session['basket'], edit_address_form = edit_address_form, edit_payment_form = edit_payment_form, user_address = user_address, user_payment_details = user_payment_details)
        
    else:
        # TODO
        # if user is not logged in
        if address_form.validate_on_submit():
            guest_address = Address(
                full_name=address_form.full_name.data,
                phone_number=address_form.phone_number.data,
                postcode=address_form.postcode.data,
                address_line_one = address_form.address_line_one.data,
                address_line_two = address_form.address_line_two.data,
                town_city=address_form.town_city.data,
                county=address_form.county.data
            )

        return render_template('checkout.html', address_form = address_form, payment_form = payment_form, basket = session['basket'], edit_address_form = edit_address_form, edit_payment_form = edit_payment_form, user_address = guest_address, user_payment_details = user_payment_details)

@app.route('/order-confirmation')
def orderConfirmationPage():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)