import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from routes.user_route import user_bp
from configs.app_config import create_database_connection
from routes.property_route import property_bp

app = Flask(__name__)
load_dotenv()

CORS(app)

db = create_database_connection(app)


@app.route("/")
def home():
    return jsonify({"success": "Hello from the server 1", 'message': "server 1 running"})


app.register_blueprint(user_bp, url_prefix="/users")

app.register_blueprint(property_bp,url_prefis="/property")

if (__name__ == "__main__"):
    app.run(debug=True, port=os.getenv("PORT"))
