from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialisation de l'application
app = Flask(__name__)

# Configuration MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/tasks_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Modèle Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, description={self.description}, is_done={self.is_done})"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_done": self.is_done
        }

# Schéma TaskSchema
class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True

# Routes de l'application
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict()), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        is_done=data.get('is_done', False)
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.is_done = data.get('is_done', task.is_done)

    db.session.commit()
    return jsonify(task.to_dict()), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

# Initialisation de la base de données
with app.app_context():
    try:
        db.create_all()
        print("Base de données initialisée avec succès.")
    except Exception as ex:
        print("Erreur lors de l'initialisation :", ex)

# Exécution de l'application
if __name__ == '__main__':
    app.run(debug=True)
