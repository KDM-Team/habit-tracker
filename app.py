from flask import Flask, jsonify
from flask_migrate import Migrate

from config import Config
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route("/")
    def index():
        return jsonify({"message": "Habit Tracker API works!"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
