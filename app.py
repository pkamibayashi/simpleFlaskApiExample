from flask import Flask, request, jsonify
from models.task import Task


app = Flask(__name__)
tasks = []
task_id = 1


@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id
    data = request.get_json()  #recupera o que o cliente envia para a gente
    new_task = Task(task_id, data['title'], data.get('description', ''), data.get('status', 'pendente'))
    task_id += 1
    tasks.append(new_task)
    return jsonify({"message": "Tarefa criada com sucesso", "task": new_task.to_dict()}), 201  #retorna o que o servidor envia para o cliente


@app.route("/get_all_tasks", methods=["GET"])
def read_all_tasks():
    return jsonify([task.to_dict() for task in tasks])


@app.route("/tasks/<int:task_id>", methods=["GET"])
def read_task(task_id):
    for task in tasks:
        if task.id == task_id:
            return jsonify(task.to_dict())
    return jsonify({"message": "Tarefa não encontrada"}), 404


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task.id == task_id:
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.status = data.get('status', task.status)
            return jsonify({"message": "Tarefa atualizada com sucesso", "task": task.to_dict()})
    return jsonify({"message": "Tarefa não encontrada"}), 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return jsonify({"message": "Tarefa removida com sucesso"})
    return jsonify({"message": "Tarefa não encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)
