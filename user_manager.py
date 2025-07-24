from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Boolean, Table, Column, ForeignKey
from flask_login import UserMixin

# todo: build the User data table here and recap on how to use sql databases!

# Creating the database
class Base(DeclarativeBase):
  pass

# the above just says every class that inherits from the Base will become a table in the database

db = SQLAlchemy(model_class=Base)

# Create the association table (to like user and product together, this table will have product_id and also the user_id
user_cart = Table(
    "user_cart",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=True) # product is an instance aka object of the Product class, and id is the attribute of that object
)

# the table above looks something like this:
"""
+---------+------------+
| user_id | product_id |
+---------+------------+
|    1    |      2     |
|    1    |      3     |
|    2    |      3     |
|    3    |      1     |
+---------+------------+
"""

# Create the user class
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    cart_items: Mapped[list['Product']] = relationship(secondary=user_cart, back_populates="users_with_product") # this list['Product'], is a type hint to show database contains a list of Product objects.
    # secondary=user_cart is to show that that is the connecting table to link up the User class and the Product class, in a many to many relationship

# Create the product class
class Product(db.Model): # note that db.Model already inherits Base, hence no need write class Product(Base):, and db.Model is compatible with flask_sqalchemy
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)
    discount: Mapped[str] = mapped_column(String(100), nullable=False)
    reviewed: Mapped[str] = mapped_column(String(100), nullable=False)
    currency: Mapped[str] = mapped_column(String(100), nullable=False, default='sgd')
    unit_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    users_with_product: Mapped[list['User']] = relationship(secondary=user_cart, back_populates="cart_items")
    # as this is a relational thing, it does NOT show up when you view the database, it is a backend thing
    # the same goes for cart_items