import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# SQLite database initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hngx2.db'

db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, name, age=None,email=None):
        self.name = name
        self.age = age
        self.email = email

# Create tables
with app.app_context():
    db.create_all()

# Create a new person
@app.route('/api', methods=['POST'])
def create_person():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')


    if not name:
        return jsonify({'error': 'Name is required'}), 400

    new_person = Person(name, age, email)
    db.session.add(new_person)
    db.session.commit()

    return jsonify({'message': 'Person created successfully'}), 201

# Get details of a person by user_id or name
@app.route('/api/<param>', methods=['GET'])
def get_person(param):
    if param.isdigit():
        # The parameter is an integer, indicating a user_id
        person = Person.query.get(int(param))
    else:
        # The parameter is not an integer, assuming it's a name
        person = Person.query.filter_by(name=param).first()

    if not person:
        return jsonify({'error': 'Person not found'}), 404

    person_data = {
        'id': person.id,
        'name': person.name,
        'age': person.age
    }
    return jsonify(person_data), 200

# Update details of an existing person by user_id
@app.route('/api/<int:user_id>', methods=['PUT'])
def update_person(user_id):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    person = Person.query.get(user_id)

    if not person:
        return jsonify({'error': 'Person not found'}), 404

    person.name = name
    person.age = age
    person.email = email
    db.session.commit()

    return jsonify({'message': 'Person updated successfully'}), 200

#Delete a person by user_id
@app.route('/api/<int:user_id>', methods=['DELETE'])
def delete_person(user_id):
        person = Person.query.filter_by(id=user_id).first()
        if person:
            db.session.delete(person)
            db.session.commit()
            return jsonify({'message': 'Person deleted successfully'}), 200
        else:
            return jsonify({'message': 'Person not found or does not exist'}), 404

if __name__ == '__main__':
    app.run(debug=True)