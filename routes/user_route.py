from flask import Blueprint, jsonify, request, Flask
from models.user_model import User
from flask_bcrypt import Bcrypt
import jwt
import time
import os

bcrypt = Bcrypt()

user_bp = Blueprint("user_blueprint", __name__)


# Get all users
@user_bp.route("/", methods=["GET"])
def get_all_users():
    try:
        # Retrieve all users from the User collection
        users = User.objects.all().to_json()
        # Return the retrieved users
        return users
    except Exception as e:
        # Handle any exceptions that occur during the operation
        print("Error retrieving users:", e)
        # Return an error message or None, depending on your requirement
        return jsonify({"message": f"Error retrieving users{e}"})


# Get a single user by ID
@user_bp.route("/<ObjectId:id>", methods=["GET"])
def get_one_user(id):
    try:
        # Find the user by its ObjectId
        user = User.objects.with_id(id)

        # If user found, return the JSON representation
        if user:
            return user
        else:
            # If user not found, return a 404 Not Found response
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        # Log the exception (handle it according to your logging setup)
        print(f"An error occurred while fetching user: {e}")

        # Return an error message and HTTP status 500 (Internal Server Error)
        return jsonify({"error": "An internal server error occurred", "message": str(e)}), 500

# Register a user


@user_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # Extract data from the request JSON
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Check if required fields are provided
        if not (username and email and password):
            return jsonify({"error": "Username, email, and password are required"}), 400

        # Generate hashed password using bcrypt
        hashed_password = bcrypt.generate_password_hash(
            password, rounds=10).decode('utf-8')

        # Check if user with provided email already exists
        existing_user = User.objects(email=email).first()
        if existing_user:
            # 409 Conflict status code
            return jsonify({"error": "Email already exists"}), 409

        # Create a new user instance
        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        # Save the new user to the database
        new_user.save()

        # Return JSON representation of the new user and HTTP status 201 (Created)
        return jsonify({"message": "User has been registered successfully", "user": new_user.to_json()}), 201

    except Exception as e:
        # Log the exception (handle it according to your logging setup)
        print(f"An error occurred while creating user: {e}")

        # Return an error message and HTTP status 500 (Internal Server Error)
        return jsonify({"error": "An internal server error occurred", "message": f"An error occurred while creating user: {e}"}), 500


# Login a user
@user_bp.route("/login", methods=["POST"])
def login_user():
    try:
        # Retrieve email and password from the request JSON data
        data = request.json
        email = data.get("email")
        password = data.get("password")

        # Retrieve the user document from the database based on the email
        user_data = User.objects(email=email).first()

        # If user with provided email doesn't exist, return error
        if user_data is None:
            return jsonify({"error": "Invalid email"}), 404

        # Retrieve the hashed password from the user document
        hashed_password = user_data.password

        # Verify the password using bcrypt
        if bcrypt.check_password_hash(hashed_password, password):
            # Convert ObjectId to string for JSON serialization
            user_id_str = str(user_data.id)

            # Generate JWT token with user payload and 7-day expiry
            payload = {
                "user_id": user_id_str,
                # Token expires in 7 days
                "exp": int(time.time()) + (7 * 24 * 60 * 60)
            }
            secret_key = os.getenv("SECRET_KEY")
            token = jwt.encode(payload, secret_key, algorithm="HS256")

            # Construct response object with user details and token
            response_obj = {
                "username": user_data.username,
                "id": user_id_str,
                "role": user_data.role
            }

            # Return success message along with token and user details
            return jsonify({"message": "Login successful", "token": token, "user": response_obj}), 200
        else:
            # If password verification fails, return error
            return jsonify({"error": "Incorrect password"}), 401

    except Exception as e:
        # Handle any unexpected errors and return error response
        return jsonify({"error": "Error while logging in", "message": str(e)}), 500
