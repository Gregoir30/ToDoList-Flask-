import unittest
from app import app, db, Task

class TestGetTasks(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()
            task = Task(title="Test Task", description="Test Description", is_done=False)
            db.session.add(task)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_get_all_tasks(self):
        response = self.app.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Test Task")

if __name__ == '__main__':
    unittest.main()
