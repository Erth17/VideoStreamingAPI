# __Video Streaming Registration and Payment Service API__

## __Requirements__
The following are required in order to run the project:

- Python 3.10 or later
- pip (Python package manager)

To install the required packages:
``` pip install flask pytest ```

## __Running the API__
From the project directory, start the Flask application:
``` python app.py ```
The API will start locally, normally at:
```  http://127.0.0.1:5000 ```

## __Running the Tests__
To execute the unit tests, run:
``` pytest ```
Pytest will automatically execute all files beginning with ```test_```

## __Available Endpoints__

### User Registration
POST - /users - Registers a new user
GET - /users - Retrieves all users and filters by available cards ```CreditCard=Yes/No```

### Payments
POST - /payments - Submits a payment with a card registered to a user

## __Notes__
This project is an assignment and for an interview and not to be used practically in real-world deployments.
