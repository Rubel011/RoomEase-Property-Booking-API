from flask import Blueprint, jsonify
from models.property_model import Property
from bson import ObjectId

property_bp = Blueprint("property_blueprint", __name__)


@property_bp.route("/", methods=["GET"])
def retrieve_all_property():
    try:
        # Retrieve all properties from the database
        properties = Property.objects().to_json()

        # Return JSON representation of all properties
        return properties, 200
    except Exception as e:
        # Log the exception (handle it according to your logging setup)
        print(f"An error occurred while retrieving properties: {e}")

        # Return an error message and HTTP status 500 (Internal Server Error)
        return jsonify({"error": "An internal server error occurred", "message": str(e)}), 500


@property_bp.route("/<ObjectId:id>", methods=["GET"])
def retrieve_property_by_id(id):
    try:
        # Retrieve the property by its ObjectId
        property = Property.objects.with_id(id).to_json()

        # If property found, return its JSON representation
        if property:
            return property, 200
        else:
            # If property not found, return a 404 Not Found response with a custom error message
            return jsonify({"error": "Property not found for the provided ID"}), 404

    except Exception as e:
        print(f"An error occurred while retrieving property: {e}")

        # Return a custom error message and HTTP status 500 (Internal Server Error)
        return jsonify({"error": "An internal server error occurred while retrieving property", "message": str(e)}), 500
