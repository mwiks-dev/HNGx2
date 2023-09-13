import unittest
import json
from app import app, db, Person

class TestCRUDOperations(unittest.TestCase):

    def setUp(self):
        # Set up a test client and create a test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        # Establish the application context
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        # Clean up the test database and pop the application context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_person(self):
        # Test creating a new person
        data = {'name': 'Mwikali', 'age': 26, 'email':'mwikali119@gmail.com'}
        response = self.app.post('/api', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['message'], 'Person created successfully')

    def test_get_person_by_user_id_or_name(self):
        # Test retrieving a person by user_id
        new_person = Person(name='Mwiks', age=25, email='mwiks@gmail.com')
        db.session.add(new_person)
        db.session.commit()

        response = self.app.get(f'/api/{new_person.id}')
        self.assertEqual(response.status_code, 200)
        person_data = json.loads(response.data)
        self.assertEqual(person_data['name'], 'Mwiks')
        self.assertEqual(person_data['age'], 25)
        # self.assertEqual(person_data['email'], 'mwiks@gmail.com')

        # Test retrieving a person by name
        response_by_name = self.app.get(f'/api/{new_person.name}')
        self.assertEqual(response_by_name.status_code, 200)
        person_data_by_name = json.loads(response_by_name.data)
        self.assertEqual(person_data_by_name['name'], 'Mwiks')
        self.assertEqual(person_data_by_name['age'], 25)
        # self.assertEqual(person_data_by_name['email'], 'mwiks@gmail.com')


    def test_update_person(self):
        # Test updating a person's details
        new_person = Person(name='Charlie', age=40, email='charlie@gmail.com')
        db.session.add(new_person)
        db.session.commit()

        updated_data = {'name': 'Charlie Brown', 'age': 45,'email':'charlie@gmail.com'}
        response = self.app.put(f'/api/{new_person.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'Person updated successfully')

    def test_delete_person(self):
        # Test deleting a person
        new_person = Person(name='David', age=50,email='david@gmail.com')
        db.session.add(new_person)
        db.session.commit()

        response = self.app.delete(f'/api/{new_person.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'Person deleted successfully')

if __name__ == '__main__':
    unittest.main()
