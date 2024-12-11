from flask import Blueprint, request, jsonify
from models import db, Task

api = Blueprint('api', __name__)

@api.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'is_done': task.is_done
    } for task in tasks])

@api.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = Task(title=data['title'], description=data.get('description'))
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created', 'id': task.id})

@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get_or_404(task_id)
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'is_done' in data:
        task.is_done = data['is_done']
    db.session.commit()
    return jsonify({'message': 'Task updated'})

@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})
