from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate

from config import Config
from models import db, Habit


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route("/")
    def index():
        return jsonify({"message": "Habit Tracker API works!"})

    with app.app_context():
        db.create_all()

    # Tworzy nowy nawyk
    @app.route('/habits', methods=['POST'])
    def create_habit():
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        new_habit = Habit(name=name, description=description)
        db.session.add(new_habit)
        db.session.commit()
        return jsonify(new_habit.to_dict()), 201

    # Zwraca liste wszystkich nawyków
    @app.route('/habits', methods=['GET'])
    def get_habits():
        habits = Habit.query.all()
        return jsonify([habit.to_dict() for habit in habits])

    @app.route('/habits/<int:habit_id>', methods=['GET'])
    def get_habit(habit_id):
        habit = Habit.query.get_or_404(habit_id)
        return jsonify(habit.to_dict())

    @app.route('/habits/<int:habit_id>', methods=['PUT','PATCH'])
    def update_habit(habit_id):
        habit = Habit.query.get_or_404(habit_id)
        data = request.get_json()
        habit.name = data.get('name', habit.name)
        habit.description = data.get('description', habit.description)
        db.session.commit()
        return jsonify(habit.to_dict())

    # Usuwa Nawyk
    @app.route('/habits/<int:habit_id>', methods=['DELETE'])
    def delete_habit(habit_id):
        habit = Habit.query.get_or_404(habit_id)
        db.session.delete(habit)
        db.session.commit()
        return jsonify({'message': 'Habit deleted successfully'})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
