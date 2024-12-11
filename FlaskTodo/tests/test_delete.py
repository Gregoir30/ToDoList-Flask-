import unittest
from app import app, db, Task

class TestDeleteTask(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()
            task = Task(title="Task to Delete", description="Task Description", is_done=False)
            db.session.add(task)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_delete_task(self):
        response = self.app.delete('/api/tasks/1')
        self.assertEqual(response.status_code, 200)

        # Vérifie que la tâche n'existe plus
        response = self.app.get('/api/tasks')
        data = response.get_json()
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()
