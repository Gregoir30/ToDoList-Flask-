import unittest
from app import app, db, Task

class TestPutTask(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()
            task = Task(title="Task to Update", description="Original Description", is_done=False)
            db.session.add(task)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_update_task(self):
        updated_task = {
            "title": "Updated Task",
            "description": "Updated Description",
            "is_done": True
        }
        response = self.app.put('/api/tasks/1', json=updated_task)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["title"], "Updated Task")
        self.assertEqual(data["is_done"], True)

if __name__ == '__main__':
    unittest.main()
