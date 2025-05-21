## Salaam Microfinance Backend

To get started, clone the repository to your local machine and install the dependencies using the command pip install -r requirements.txt. Make sure you have Python and pip installed. After installing dependencies, initialize the database by running the migration commands or using a seeding script if provided. Then start the Flask app with python app.py.

This project defines two main data models: Customer and Transaction. The Customer model stores customer information such as name, email, phone number (unique), account status, and balance, and links to their transactions. The Transaction model records financial transactions like deposits or withdrawals, including type, amount, timestamp, and references the associated customer. Both models support serialization for easy JSON output, helping you manage and manipulate customer and transaction data efficiently.

The backend provides RESTful API routes to perform CRUD operations on customers and transactions. You can create, read, update, and delete customers, and view all transactions related to customers. These APIs enable interaction with the database through HTTP requests, which you can test using tools like Thunder Client or Postman for seamless integration and development.

## API Documentation
The backend exposes RESTful endpoints to manage customer and transaction data:

Customer Routes
GET /customers
Retrieve a list of all customers.

GET /customers/<id>
Get details of a specific customer by ID.

POST /customers
Create a new customer.
Request Body: JSON with name, email, phone, account_status (optional), and balance (optional).

PATCH /customers/<id>
Update an existing customer’s data partially.
Request Body: JSON with any of the customer fields to update.

DELETE /customers/<id>
Delete a customer by ID.

Transaction Routes
GET /transactions
Retrieve all transactions with customer details included.

(Additional CRUD routes for transactions can be added similarly as needed.)

You can test these endpoints using API clients like Thunder Client, Postman, or via curl commands to verify data creation, retrieval, updating, and deletion.
