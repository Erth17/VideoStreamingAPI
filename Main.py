from flask import Flask, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)
#GET
#POST
#PUT
#DELETE

# Temporary storage
users = []

def validate_email(email):
    pass

def validate_date(date):
    pass

@app.route('/')
def home():
    return "Home"

@app.route('/get-user/<user_id>')
def get_user(user_id):
    user_data = {
        'user_id': user_id,
        'name' : 'James',
        'email' : '<EMAIL>'
    }

    extra = request.args.get('extra')
    if extra:
        user_data['extra'] = extra

    return jsonify(user_data), 200

@app.route('/create-user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        user_data = request.get_json()

    return jsonify(user_data), 201

@app.route('/users', methods=['POST'])
def register_users():
    data = request.get_json()

    if not data:
        # If the request body fails to satisfy any of the basic validation checks
        # return HTTP Status code: 400
        return jsonify({}), 400

    required_fields = [
        'username',
        'password',
        'email',
        'DoB']

    optional_fields = [
        'card_number',
    ]

    missing = [field for field in required_fields if field not in data]

    if missing:
        # If the request body fails to satisfy any of the basic validation checks
        # return HTTP Status code: 400
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    username = data['username']
    password = data['password']
    email = data['email']
    dob = data['DoB']
    card_number = data['card_number']

    if not validate_email(email):
        pass

    if not validate_date(dob):
        pass

    if any(user["username"] == username for user in users):
        # If the username has already been used
        # reject the request and return HTTP Status code: 409
        return jsonify({"error": f"Username already exists"}), 409

    user = {
        "username": username,
        "email": email,
        "password": password, # Obviously hashed
        "dob": dob,
        "card_number": card_number, # Obviously hashed
    }

    users.append(user)

    return jsonify({
        # A successful action should return HTTP Status code: 201
        "message": "User created",
        "user_id": user["id"],
    }), 201


if __name__ == '__main__':
    app.run(debug=True)