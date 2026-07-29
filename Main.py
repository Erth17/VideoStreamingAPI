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

def validate_username(username):
    # alphanumeric, no spaces
    return re.fullmatch(r"[A-Za-z0-9]+", username) is not None

def validate_password(password):
    # min length 8, at least one upper case letter & number
    if len(password) <= 8 or not re.search(r"[A-Z]", password) or not re.search(r"\d", password):
        return False
    return True

def validate_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None

def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def calculate_age(date_of_birth):
    dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    today = datetime.today().date()

    age = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    return age

def validate_card_number(card_number):
    # If given should have 16 digits.
    return re.fullmatch(r"\d{16}", card_number) is not None

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
    card_number = data.get('card_number')

    if not validate_username(username):
        # Fails to satisfy valid username format
        # return HTTP Status code: 400
        return jsonify({
            'error': "Username must only contain alphanumeric characters."
        }), 400

    if not validate_password(password):
        # Fails to satisfy valid password format
        # return HTTP Status code: 400
        return jsonify({
            'error': "Password must be longer than 8 characters and contain" +
                     " at least one uppercase letter and one number."
        }), 400

    if not validate_email(email):
        # Fails to satisfy valid email format
        # return HTTP Status code: 400
        return jsonify({
            'error': f"Invalid email: {email}"
        }), 400

    if not validate_date(dob):
        # Fails to satisfy valid ISO 8601 format
        # return HTTP Status code: 400
        return jsonify({
            'error': "Please enter date of birth in YYYY-MM-DD format."
        }), 400

    if calculate_age(dob) < 18:
        # Reject requests if the user is under the age of 18
        # return HTTP Status code: 403
        return jsonify({
            'error': "You must be at least 18 years old to register."
        }), 403

    if card_number is not None and not validate_card_number(card_number):
        # Fails to satisfy valid card number length
        # return HTTP Status code: 400
        return jsonify({
            'error': "Card number should have 16 digits."
        }), 400

    if any(user["username"] == username for user in users):
        # If the username has already been used, reject the request
        # return HTTP Status code: 409
        return jsonify({
            "error": f"Username already exists"
        }), 409

    user = {
        "username": username,
        "email": email,
        "password": password, # Obviously hashed later
        "dob": dob,
        "card_number": card_number, # Obviously hashed later
    }

    users.append(user)

    return jsonify({
        # A successful action should return HTTP Status code: 201
        "message": "User created",
        "user_id": user["id"],
    }), 201

@app.route("/users", methods=['GET'])
def get_users():
    card_filter = request.args.get("card_filter")

    if card_filter is None:
        filtered_users = users

    elif card_filter.lower() == "yes":
        filtered_users = [user for user in users if user.get("card_number")]

    elif card_filter.lower() == "no":
        filtered_users = [user for user in users if not user.get("card_number")]

    else:
        return jsonify({
            'error': "Card filter must be either yes or no."
        }), 400

    response = []

    for user in filtered_users:
        response.append({
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "dob": user["dob"],
            "has_card_number": bool(user.get("card_number"))
        })

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)