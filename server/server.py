from db import db_init
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    load_dotenv()
    # Initialize the database
    db_init()

    from routes import register_blueprints
    register_blueprints(app)

    @app.route("/")
    def index():
        return "connected"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
