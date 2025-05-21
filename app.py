from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Customer, Transaction, Admin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///salaam.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'your_secret_key_here'  # Needed for session management

CORS(app, supports_credentials=True)
migrate = Migrate(app, db)
db.init_app(app)

# ADMIN LOGIN
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username, password=password).first()
    if admin:
        session['admin_id'] = admin.id
        return jsonify({"message": "Admin logged in successfully"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_id', None)
    return jsonify({"message": "Admin logged out successfully"})

# CUSTOMER CRUD - simple inline admin session check
@app.route('/customers', methods=['POST'])
def create_customer():
    if not session.get('admin_id'):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    try:
        # Check if email or phone already exists
        if Customer.query.filter_by(email=data['email']).first():
            return jsonify({"error": "A customer with this email already exists"}), 400
        if Customer.query.filter_by(phone=data['phone']).first():
            return jsonify({"error": "A customer with this phone number already exists"}), 400

        customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            account_status=data.get('account_status', 'active'),
            balance=data.get('balance', 0.0)
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route('/customers', methods=['GET'])
def get_customers():
    if not session.get('admin_id'):
        return jsonify({"error": "Unauthorized"}), 401

    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers]), 200

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    if not session.get('admin_id'):
        return jsonify({"error": "Unauthorized"}), 401

    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_dict()), 200

@app.route('/customers/<int:id>', methods=['PATCH'])
def update_customer(id):
    if not session.get('admin_id'):
        return jsonify({"error": "Unauthorized"}), 401

    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    try:
        if 'name' in data:
            customer.name = data['name']
        if 'email' in data:
            customer.email = data['email']
        if 'phone' in data:
            customer.phone = data['phone']
        if 'account_status' in data:
            customer.account_status = data['account_status']
        if 'balance' in data:
            customer.balance = data['balance']

        db.session.commit()
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    if not session.get('admin_id'):
        return jsonify({"error": "Unauthorized"}), 401

    customer = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# View Transaction History - simple inline admin session check
@app.route('/transactions', methods=['GET'])
def admin_get_transactions():
    if not session.get('admin_id'):
        return jsonify({"error": "Unauthorized"}), 401

    transactions = Transaction.query.all()
    transactions_list = [t.to_dict() for t in transactions]
    return jsonify(transactions_list), 200

@app.route('/transactions/<int:id>', methods=['GET'])
def get_transaction_by_id(id):
    transaction = Transaction.query.get(id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify(transaction.to_dict()), 200


if __name__ == '__main__':
    app.run(debug=True)
