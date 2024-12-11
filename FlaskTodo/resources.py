from flask_restful import Resource
from models import Task
from schemas import TaskSchema


class TaskResource(Resource):
    task_schema = TaskSchema()
    task_list_schema = TaskSchema(many=True)

    def get(self, task_id=None):
        if task_id:
            task = Task.query.get_or_404(task_id)
            return self.task_schema.dump(task), 200
        else:
            all_tasks = Task.query.all()
            return self.task_list_schema.dump(all_tasks), 200
