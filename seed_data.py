from app import app
from models import db, Food

foods = [
    {"id": 1, "name": "Cheeseburger", "price": 6.99, "image": "/static/images/cheese-burger.jpg", "category": "Burgers"},
    {"id": 2, "name": "Veggie Pizza", "price": 8.49, "image": "/static/images/veggie-pizza.jpg", "category": "Pizza"},
    {"id": 3, "name": "Chicken Wrap", "price": 5.99, "image": "/static/images/chicken-wrap.jpg", "category": "Wraps"},
    {"id": 4, "name": "Pasta Alfredo", "price": 7.99, "image": "/static/images/pasta-alfreddo.jpg", "category": "Pasta"},
    {"id": 5, "name": "French Fries", "price": 3.49, "image": "/static/images/french-fries.jpg", "category": "Sides"},
    {"id": 6, "name": "Chicken Biryani", "price": 7.0, "image": "/static/images/chicken-biryani.jpg", "category": "Biryani"},
    {"id": 7, "name": "Beef Burger", "price": 4.0, "image": "/static/images/burger.jpg", "category": "Fast Food"},
    {"id": 8, "name": "Double Beef Burger", "price": 10.0, "image": "/static/images/burger.jpg", "category": "Burger"},
    {"id": 9, "name": "Beef Wrap", "price": 7.0, "image": "/static/images/wrap.jpg", "category": "Wrap"}
]
with app.app_context():
    for food in foods:
        existing = Food.query.filter_by(name=food["name"]).first()
        if not existing:
            item = Food(
                name=food["name"],
                price=food["price"],
                image=food["image"],
                category=food["category"]
            )
            db.session.add(item)
    db.session.commit()
    print("✅ Food items seeded successfully!")