# 🛒 Ecommerce Flask App

A beginner-friendly ecommerce web app built with [Flask](https://flask.palletsprojects.com/), [Bootstrap 5](https://getbootstrap.com/), and [Stripe Checkout](https://stripe.com/docs/checkout). It lets users browse products, add them to a cart, and pay using Stripe — all while following clean design and code practices.

---

## ✅ What You’ll Learn

This project includes several practical web development techniques:

* **[Flask routing](https://flask.palletsprojects.com/en/latest/quickstart/#routing)**: dynamic URLs with product IDs and success/cancel paths.
* **[Jinja templating](https://jinja.palletsprojects.com/en/latest/templates/)**: reusable templates with layout inheritance and conditional logic.
* **[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/latest/)**: object-relational mapping and data models.
* **[Flask-Login](https://flask-login.readthedocs.io/en/latest/)**: session-based authentication and protected views.
* **[Bootstrap grid system](https://getbootstrap.com/docs/5.3/layout/grid/)**: responsive layout and card-based product display.
* **[Stripe Checkout Sessions](https://stripe.com/docs/checkout/quickstart)**: server-side API for secure payment links.
* **[Jinja filters](https://jinja.palletsprojects.com/en/latest/templates/#builtin-filters)** like `format` for price display (`"%.2f"|format(...)`).
* **Flask flash messages** for user feedback.
* Using [`url_for(..., _external=True)`](https://flask.palletsprojects.com/en/latest/api/#flask.url_for) to generate absolute URLs required by third-party services like Stripe.

---

## 🧰 Libraries & Tools Used

* [Flask](https://flask.palletsprojects.com/): lightweight Python web framework.
* [Bootstrap 5](https://getbootstrap.com/): frontend styling framework.
* [Stripe API](https://stripe.com/docs/api): handles payment processing and secure checkout.
* [Flask-Bootstrap](https://bootstrap-flask.readthedocs.io/en/stable/): integrates Bootstrap with Flask templates.
* [Flask-Login](https://flask-login.readthedocs.io/): session and user management.
* [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/): ORM wrapper around SQLAlchemy.
* [Werkzeug](https://werkzeug.palletsprojects.com/): used under Flask for request/response handling and security.
* Fonts: The site uses [Bootstrap Icons](https://icons.getbootstrap.com/) for star ratings and UI icons.

---

## 📁 Project Structure

```
.
├── static/
│   └── images/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── shop.html
│   ├── cart.html
│   ├── success.html
│   └── cancelled.html
├── .env
├── main.py
├── user_manager.py
└── requirements.txt
```

### Notes:

* `static/images/`: contains image assets like product photos.
* `templates/`: all the Jinja HTML templates.
* [`user_manager.py`](./user_manager.py): defines `User`, `Product`, and the `user_cart` relationship model.
* [`main.py`](./main.py): app logic, route handlers, Stripe integration.
* `.env`: stores Stripe keys and Flask secret key (not included in Git for security).
* [`requirements.txt`](./requirements.txt): dependency list for recreating the environment.
