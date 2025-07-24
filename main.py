import os, stripe
from dotenv import load_dotenv
from user_manager import db, User, Product, user_cart
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from flask_bootstrap import Bootstrap5

load_dotenv()

app = Flask(__name__)
stripe.api_key = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
Bootstrap5(app) # this is for WTForms otherwise have the type the bootstrap code out manually

# Database set-up
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Eshop_website.db"
db.init_app(app)

# Set up Flask to use Flask-Login.
# This makes the 'current_user' object available in ALL templates automatically.
login_manager = LoginManager()
login_manager.init_app(app)

# Define logged_in function
def logged_in(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return function(*args, **kwargs)
        else:
            abort(403)
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

with app.app_context():
    db.create_all()

    # # Add products first:
    # product_1 = Product(
    #     img_url="https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2338&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    #     discount='False',
    #     reviewed='False',
    #     unit_amount=2000,
    #     name='Custom Python Script', )
    #
    # product_2 = Product(
    #     img_url="https://images.unsplash.com/photo-1573867639040-6dd25fa5f597?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    #     discount='True',
    #     reviewed='True',
    #     unit_amount=10000,
    #     name='Custom Python Website', )
    #
    # product_3 = Product(
    #     img_url="https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    #     discount='True',
    #     reviewed='False',
    #     unit_amount=13000,
    #     name='Custom Python Game', )
    #
    # db.session.add_all([product_1, product_2, product_3])
    # db.session.commit()

    ### MEGA NOTE: db.get_or_404(id) can only be used IN FLASK ROUTES, using this outside of flask routes will give you an error!
    # for num in range(4, 9 + 1):
    #     product_to_delete = Product.query.get(num)
    #     if product_to_delete:
    #         db.session.delete(product_to_delete)
    #         db.session.commit()

PRODUCTS = [
        {
            'img_url': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=2338&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'discount': 'False',
            'reviewed': 'False',
            'api_data': {
                'price_data': {
                    'currency': 'sgd',
                    'unit_amount': 2000,  # $20.00
                    'product_data': {
                        'name': 'Custom Python Script',
                    },
                },
                'quantity': 1,
            }
        },
        {
            'img_url': 'https://images.unsplash.com/photo-1573867639040-6dd25fa5f597?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'discount': 'True',
            'reviewed': 'True',
            'api_data':{
                'price_data': {
                    'currency': 'sgd',
                    'unit_amount': 10000,  # $100.00
                    'product_data': {
                        'name': 'Custom Python Website',
                    },
                },
                'quantity': 1,
            }
        },
        {
            'img_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'discount': 'True',
            'reviewed': 'False',
            'api_data': {
                'price_data': {
                    'currency': 'sgd',
                    'unit_amount': 13000,  # $130.00
                    'product_data': {
                        'name': 'Custom Python Game',
                    },
                },
                'quantity': 1,
            }
        }
    ]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/shop")
def shop():
    # List of dictionaries of products
    result = db.session.execute(db.select(Product).order_by(Product.id))
    product_list = result.scalars()
    return render_template("shop.html", products=product_list)

@app.route("/add_to_cart/<int:product_id>", methods=['POST'])
@logged_in
def add_to_cart(product_id):
    product_added_to_cart = db.get_or_404(Product, product_id)
    if product_added_to_cart not in current_user.cart_items:
        current_user.cart_items.append(product_added_to_cart) # this is because cart_items is a LIST, as defined in the User object
        db.session.commit()
    else:
        flash("Item already in cart, try adding other items instead.")
    return redirect(url_for('shop'))

@app.route("/cart")
@logged_in
def cart():
    number_of_items = len(current_user.cart_items)
    total_amount = 0
    for product in current_user.cart_items:
        total_amount += product.unit_amount
    return render_template("cart.html", total_amount=total_amount, num_products=number_of_items)

@app.route("/checkout_cart", methods=['POST'])
@logged_in
def checkout_cart():
    products_in_cart = current_user.cart_items
    line_items = [
        {
            'price_data': {
                'currency': product_to_buy.currency,
                'unit_amount': product_to_buy.unit_amount,  # $130.00
                'product_data': {
                    'name': product_to_buy.name,
                },
            },
            'quantity': product_to_buy.quantity,
        } for product_to_buy in products_in_cart
    ]

    session = stripe.checkout.Session.create(payment_method_types=['card'],
                                             line_items=line_items,
                                             mode='payment',
                                             success_url=url_for('success', _external=True, from_checkout='True'),
                                             # _external=True returns the absolute URL which is needed to direct users
                                             # to a third party service, instead of relative urls, which url_for() alone generates.
                                             # eg. url_for('success') -> '/success'
                                             cancel_url=url_for('cancel', _external=True, from_checkout='True'))
    return redirect(session.url)

@app.route("/delete_from_cart/<int:product_id>", methods=["POST"])
@logged_in
def delete_from_cart(product_id):
    product_to_remove = db.get_or_404(Product, product_id)
    current_user.cart_items.remove(product_to_remove)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route("/checkout/<int:product_id>", methods=['POST'])
def checkout(product_id):
    product_to_buy = db.get_or_404(Product, product_id)
    session = stripe.checkout.Session.create(payment_method_types=['card'],
                                             line_items=[
                                                 {
                                                     'price_data': {
                                                         'currency': product_to_buy.currency,
                                                         'unit_amount': product_to_buy.unit_amount,  # $130.00
                                                         'product_data': {
                                                             'name': product_to_buy.name,
                                                         },
                                                     },
                                                     'quantity': product_to_buy.quantity,
                                                 }
                                             ],
                                             mode='payment',
                                             success_url=url_for('success', _external=True, from_checkout='True'),
                                             # _external=True returns the absolute URL which is needed to direct users
                                             # to a third party service, instead of relative urls, which url_for() alone generates.
                                             # eg. url_for('success') -> '/success'
                                             cancel_url=url_for('cancel', _external=True, from_checkout='True'))
    return redirect(session.url)


@app.route('/success')
def success():
    if request.args.get('from_checkout') == 'True':
        # why check for the string 'True' and not boolean True? cannot pass arguments with Boolean values because even if you do, the url is a string, so that boolean value will get converted into a string.
        if current_user.is_authenticated:
            total_products = len(current_user.cart_items)
            for num in range(total_products):
                current_user.cart_items.remove(current_user.cart_items[-1])
                db.session.commit()
        return render_template('success.html')
    else:
        return "", 404


@app.route('/cancel')
def cancel():
    if request.args.get('from_checkout') == 'True':
        return render_template('cancelled.html')
    else:
        return "", 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_email = request.form.to_dict()["email"]
        user_password = request.form.to_dict()["password"]
        existing_user = db.session.execute(db.select(User).where(User.email == user_email)).scalar()
        if existing_user:
            if check_password_hash(pwhash=existing_user.password, password=user_password) is True:
                login_user(existing_user)
                return redirect("/shop")
            else:
                flash("The password is incorrect. Please try again.")
        else:
            flash("That email does not exist. Please register.")
            return redirect("/register")

    return render_template("login.html")

@app.route("/logout")
@logged_in
def logout():
    logout_user()
    return redirect("/")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        user_email = request.form.to_dict()["email"]
        user_password = request.form.to_dict()["password"]
        print(user_password)
        if db.session.execute(db.select(User).where(User.email == user_email)).scalar():
            # scalar returns just ONE value, scalars can return MULTIPLE, its a list
            flash("You've already signed up with that email, log in instead!")
            # we must also include the flash message in our template so that the message will show.
            # the 'with' keyword in jinja just creates a temporary variable, 'messages' that exists only inside that code block, and will be gone once the end of the code block is reached
            return redirect(url_for('login'))
            # instead of using url_for can also use '/login' directly
        else:
            encrypted_password = generate_password_hash(user_password, method="pbkdf2:sha256", salt_length=8)
            new_user = User(email=user_email, password=encrypted_password)
            db.session.add(new_user)
            db.session.commit()
            flash("User created! Please sign in.")
            return redirect("/login")

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)