from db import db_init
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Initialize the database
    db = db_init()

    from routes import register_blueprints
    register_blueprints(app)

    @app.route("/")
    def index():
        return "connected"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
