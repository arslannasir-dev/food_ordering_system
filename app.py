from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Food, Order, User, OrderItem, initialize_database
from datetime import datetime
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
initialize_database(app)

# Create tables once at startup
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    foods = Food.query.all()
    return render_template('menu.html', foods=foods)

@app.route('/add_food', methods=['POST'])
def add_food():
    try:
        data = request.get_json(force=True)
        new_food = Food(
            name=data.get('name'),
            price=float(data.get('price')),
            image=data.get('image'),
            category=data.get('category')
        )
        db.session.add(new_food)
        db.session.commit()
        return jsonify({"message": "Food added successfully!"}), 201
    except Exception as e:
        print("Error adding food:", e)
        return jsonify({"error": str(e)}), 400

@app.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
    order = Order(customer_name=data['customer_name'], items=data['items'], total=data['total'])
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order placed successfully!"}), 201

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/guest_checkout', methods=['GET', 'POST'])
def guest_checkout():
    if request.method == 'POST':
        data = request.get_json()

        # Extract client details
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        cart_items = data.get('cart_items', [])
        total = float(data.get('total', 0))

        # === Validation Rules ===
        if not re.match(r".+@.+\.com$", email):
            return jsonify({"error": "Invalid email format"}), 400

        if not re.match(r"^\d{11}$", phone):
            return jsonify({"error": "Phone number must be 11 digits"}), 400

        if not first_name or not last_name or not address:
            return jsonify({"error": "Missing required fields"}), 400

        # === Create Order ===
        new_order = Order(
            user_id=None,
            customer_name=f"{first_name} {last_name}",
            email=email,
            phone=phone,
            address=address,
            total_amount=total,
            created_at=datetime.utcnow(),
            is_guest=True
        )
        db.session.add(new_order)
        db.session.commit()

        # === Add Order Items ===
        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                food_id=item.get('id'),
                quantity=item.get('quantity'),
                price=float(item.get('price'))
            )
            db.session.add(order_item)

        db.session.commit()
        print(f"✅ Guest order saved: {new_order.id}")

        return jsonify({"success": True, "order_id": new_order.id}), 200

    return render_template('guest_checkout.html')

@app.route('/register_checkout', methods=['GET', 'POST'])
def register_checkout():
    if request.method == 'POST':
        data = request.get_json()

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        password = data.get('password')
        cart_items = data.get('cart_items', [])
        total = float(data.get('total', 0))

        # === Validation Rules ===
        import re
        if not re.match(r".+@.+\.com$", email):
            return jsonify({"error": "Invalid email format"}), 400

        if not re.match(r"^\d{11}$", phone):
            return jsonify({"error": "Phone number must be 11 digits"}), 400

        if not first_name or not last_name or not address or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # === Check for existing email ===
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

        # === Create new user ===
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            password=password,
            type='client'
        )
        db.session.add(new_user)
        db.session.commit()

        # === Create order linked to this user ===
        new_order = Order(
            user_id=new_user.id,
            customer_name=f"{first_name} {last_name}",
            email=email,
            phone=phone,
            address=address,
            total_amount=total,
            is_guest=False
        )
        db.session.add(new_order)
        db.session.commit()

        # === Add order items ===
        for item in cart_items:
            # Convert ID safely to int
            try:
                food_id = int(item.get('id')) if item.get('id') else None
            except (ValueError, TypeError):
                food_id = None
            # Fallback lookup if ID missing or invalid
            food = None
            if food_id:
                food = Food.query.get(food_id)
            elif item.get('name'):
                food = Food.query.filter_by(name=item['name']).first()
            if not food:
                print(f"⚠️ Food not found or invalid ID for item: {item}")
                continue
            order_item = OrderItem(
                order_id=new_order.id,
                food_id=food.id,
                quantity=int(item.get('quantity', 1)),
                price=float(item.get('price', 0))
            )
            db.session.add(order_item)
        db.session.commit()

        print(f"✅ New user + order created: {new_user.email}")
        return jsonify({"success": True, "order_id": new_order.id}), 200

    return render_template('register_checkout.html')

@app.route('/login_checkout', methods=['GET', 'POST'])
def login_checkout():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        cart_items = data.get('cart_items', [])
        total = float(data.get('total', 0))

        print("🔐 Login attempt:", email)

        # Validate fields
        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        # Find user
        user = User.query.filter_by(email=email, password=password).first()
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        # === If user is admin, just redirect (no order) ===
        if user.type == 'admin':
            print("👑 Admin logged in successfully")
            return jsonify({"admin": True, "redirect": "/admin_dashboard"})

        # === If user is a client, place order ===
        new_order = Order(
            user_id=user.id,
            customer_name=f"{user.first_name} {user.last_name}",
            email=user.email,
            phone=user.phone,
            address=user.address,
            total_amount=total,
            is_guest=False
        )
        db.session.add(new_order)
        db.session.commit()

        # Add order items
        for item in cart_items:
            try:
                food_id = int(item.get('id')) if item.get('id') else None
            except (ValueError, TypeError):
                food_id = None

            food = None
            if food_id:
                food = Food.query.get(food_id)
            elif item.get('name'):
                food = Food.query.filter_by(name=item['name']).first()

            if not food:
                print(f"⚠️ Food not found or invalid ID for item: {item}")
                continue

            order_item = OrderItem(
                order_id=new_order.id,
                food_id=food.id,
                quantity=int(item.get('quantity', 1)),
                price=float(item.get('price', 0))
            )
            db.session.add(order_item)
        db.session.commit()

        print(f"✅ Order placed successfully by {user.email}")
        return jsonify({"success": True, "redirect": "/thankyou"})

    return render_template('login_checkout.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        print("👑 Admin login attempt:", email)

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        # Verify admin credentials
        admin = User.query.filter_by(email=email, password=password, type='admin').first()
        if not admin:
            print("❌ Invalid admin login.")
            return jsonify({"error": "Invalid admin credentials"}), 401

        print("✅ Admin authenticated:", admin.email)
        return jsonify({"success": True, "redirect": "/admin_dashboard"})

    return render_template('admin_login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    users = User.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    order_items = OrderItem.query.all()

    # ✅ Convert Order objects into JSON-safe dictionaries
    order_list = []
    for o in orders:
        order_list.append({
            "id": o.id,
            "user_id": o.user_id,
            "customer_name": o.customer_name,
            "email": o.email,
            "phone": o.phone,
            "address": o.address,
            "total_amount": float(o.total_amount or 0),
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else "",
            "is_guest": bool(o.is_guest),
            "status": o.status
        })

    return render_template(
        'admin_dashboard.html',
        users=users,
        orders=orders,
        order_items=order_items,
        orders_json=order_list  # ✅ pass this version for Chart.js
    )




if __name__ == '__main__':
    app.run(debug=True)

