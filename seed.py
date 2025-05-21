from app import app, db
from models import Admin, Customer, Transaction
from datetime import datetime
import random

def seed_data():
    with app.app_context():
        db.create_all()

        # Clear old data
        Transaction.query.delete()
        Customer.query.delete()
        Admin.query.delete()
        db.session.commit()

        # Seed admin
        admin = Admin(username='admin', password='admin123')  # plain text for demo
        db.session.add(admin)

        # Seed customers
        customers = [
            Customer(name='Mucsin Yusuf', email='mucsin@example.com', phone='0703549589'),
            Customer(name='Ali Omar', email='ali@example.com', phone='0712345678'),
            Customer(name='Fatma Noor', email='fatma@example.com', phone='0722233445'),
        ]
        db.session.add_all(customers)
        db.session.commit()

        # Seed transactions for each customer
        transaction_types = ['deposit', 'withdrawal']

        for customer in customers:
            for _ in range(3):  # 3 transactions each
                tx = Transaction(
                    type=random.choice(transaction_types),
                    amount=round(random.uniform(100, 1000), 2),
                    timestamp=datetime.utcnow(),
                    customer_id=customer.id
                )
                db.session.add(tx)

        db.session.commit()
        print("✅ Seeded admin, customers, and transactions.")

if __name__ == "__main__":
    seed_data()
