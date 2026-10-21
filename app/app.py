from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import time

app = Flask(__name__)

# Define the database URI based on the environment
if os.getenv("TESTING") == "True":
    # If testing, use in-memory SQLite
    db_uri = "sqlite:///:memory:"
else:
    # Otherwise, build the PostgreSQL URI
    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_uri = f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks]), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    task = Task(title=data["title"], done=False)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    data = request.get_json()
    if "title" in data:
        task.title = data["title"]
    if "done" in data:
        task.done = data["done"]
    db.session.commit()
    return jsonify(task.to_dict()), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "task deleted"}), 200


def init_db():
    """Tenta conectar ao banco até ele estar pronto."""
    retries = 10
    while retries > 0:
        try:
            with app.app_context():
                db.create_all()
            print("Database initialized.")
            return
        except Exception as e:
            print(f"Database not ready, retrying... ({retries} left)")
            retries -= 1
            time.sleep(3)
    raise RuntimeError("Could not connect to the database.")

@app.route("/tasks/<int:task_id>/complete", methods=["PATCH"])
def task_done(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    db.session.done(task)
    db.session.commit()
    return jsonify({"message": "task completed"}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)