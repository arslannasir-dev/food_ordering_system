from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ======================================================
# USER TABLE
# ======================================================
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), default='client')  # 'client' or 'admin'

    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} ({self.type})>"


# ======================================================
# FOOD TABLE (already exists)
# ======================================================
class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(250))
    category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Food {self.name} - ${self.price}>"


# ======================================================
# ORDER TABLE
# ======================================================
class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    customer_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(11), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_guest = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='Pending')

    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.id} - ${self.total_amount}>"


# ======================================================
# ORDER ITEM TABLE
# ======================================================
class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    food = db.relationship('Food')

    def __repr__(self):
        return f"<OrderItem {self.food.name} x{self.quantity}>"

# ======================================================
# INITIAL SETUP FUNCTION
# ======================================================
def initialize_database(app):
    """Creates tables and ensures admin exists."""
    with app.app_context():
        db.create_all()

        # Check for admin user
        existing_admin = User.query.filter_by(email='danish@gmail.com').first()
        if not existing_admin:
            admin = User(
                first_name='Danish',
                last_name='Muzzafar',
                email='danish@gmail.com',
                phone='12123456789',
                address='Birmingham',
                password='admin',
                type='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created: danish@gmail.com / admin")
        else:
            print("ℹ️ Admin already exists — skipping creation.")
