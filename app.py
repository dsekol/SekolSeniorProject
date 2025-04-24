# app.py
from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes import bp as main_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize the database with the app.
db.init_app(app)

# Create database tables if they don't exist.
with app.app_context():
    db.create_all()

# Register the Blueprint from routes.py.
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
