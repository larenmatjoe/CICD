from flask import Blueprint, jsonify, request

main = Blueprint("main", __name__)

_users = []
_user_id_counter = [0]


@main.route("/")
def index():
    return jsonify({"message": "Welcome to the Flask web server!"})


@main.route("/health")
def health():
    return jsonify({"status": "ok"})


@main.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": _users})


@main.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    _user_id_counter[0] += 1
    user = {"id": _user_id_counter[0], "name": data["name"]}
    _users.append(user)
    return jsonify({"user": user}), 201
