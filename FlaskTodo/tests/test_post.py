import unittest
from app import app, db

class TestPostTask(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_create_task(self):
        new_task = {
            "title": "New Task",
            "description": "New Task Description"
        }
        response = self.app.post('/api/tasks', json=new_task)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)  # Vérifie que l'ID est retourné
        self.assertEqual(data["title"], "New Task")

if __name__ == '__main__':
    unittest.main()
