from flask import Flask, jsonify, request
from flask_migrate import Migrate

from config import Config
from models import db, Habit


#Funckaj która zwraca nową instancje aplikacji Flask
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    #podłączamy SQLAlchemy do aplikacji Flask.
    db.init_app(app)
    migrate = Migrate(app, db)
    
    #Definiujemy prosta trasę, po wejściu zwraca JSON
    @app.route("/")
    def index():
        return jsonify({"message": "Habit Tracker API works!"})

    
    # Tworzenie bazy danych przy pierwszym uruchomieniu
    with app.app_context():
        db.create_all()
        
        
    #Tworzy nowy nawyk
    @app.route('/habits', methods=['POST'])
    def create_habit():
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        #Tworzy nowy obiekt Habit, dodaje go do sesji DB
        new_habit = Habit(name=name, description=description)
        db.session.add(new_habit)
        db.session.commit()
        return jsonify(new_habit.to_dict()), 201

    #Zwraca liste wszystkich nawyków
    @app.route('/habits', methods=['GET'])
    def get_habits():
        #Pobiera wszytskie rekordy z tabeli Habit
        habits = Habit.query.all()
        #Serializuje każdy nawyk do słownika przez to_dict()
        return jsonify([habit.to_dict() for habit in habits])

    #Pobiera konkretny nawyk po id
    @app.route('/habits/<int:habit_id>', methods=['GET'])
    def get_habit(habit_id):
        #jesli nie ma takiego id, zwraca błąd
        habit = Habit.query.get_or_404(habit_id)
        return jsonify(habit.to_dict())

    #Aktulizuje wybrany nawyk
    @app.route('/habits/<int:habit_id>', methods=['PUT', 'PATCH'])
    def update_habit(habit_id):
        #Znajduje nawyk po id albo zwraca błąd
        habit = Habit.query.get_or_404(habit_id)
        data = request.get_json()
        #Aktualizuje name and description
        habit.name = data.get('name', habit.name)
        habit.description = data.get('description', habit.description)
        db.session.commit()
        return jsonify(habit.to_dict())
    
    #Usuwa Nawyk
    @app.route('/habits/<int:habit_id>', methods=['DELETE'])
    def delete_habit(habit_id):
        #Usuwa nawyk lub zwraca błąd
        habit = Habit.query.get_or_404(habit_id)
        db.session.delete(habit)
        db.session.commit()
        return jsonify({'message': 'Habit deleted successfully'})
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)