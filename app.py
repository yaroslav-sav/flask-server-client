import itertools
from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

def read_json():
    try:
        with open("notes.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

notes = read_json()

def find_max_id(notes_dict) -> int:
    notes_id = [n["id"] for n in notes_dict]
    notes_id.append(0)
    return max(notes_id)
note_ids = itertools.count(find_max_id(read_json()) + 1)

def write_to_json(obj: dict):
    data = read_json()
    data.append(obj)
    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(data, f)

def update_all_json(obj: list):
    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(obj, f)

def find_note(note_id, notes_dict):
    for note in notes_dict:
        if note["id"] == note_id:
            return note
    return None

def get_index(notes_list, key, item):
    idx = 0
    for note in notes_list:
        if note[key] == item:
            return idx
        idx += 1
    return None

@app.get("/")
def index():
    return "<h1>Гостевая книга</h1>"

def get_int(str_value):
    try:
        return int(str_value)
    except ValueError:
        return None

@app.get("/notes")
def list_notes():
    notes_new = read_json()
    sort_args = ["id", "likes"]
    sort_arg = request.args.get("sort")
    if sort_arg is None:
        sort_arg = "id"
    elif sort_arg and (sort_arg not in sort_args or not isinstance(sort_arg, str)):
        return jsonify(error="field 'sort' is unknown or it is not a string"), 400

    order_args = ["asc", "desc"]
    order_arg = request.args.get("order")
    if order_arg is None:
        order_arg = "asc"
    elif order_arg not in order_args or not isinstance(order_arg, str):
        return jsonify(error="field 'order' is unknown or it is not a string"), 400

    def sort_notes(notes_dict, sort_arg_type, order_type):
        if order_type == "desc":
            return sorted(notes_dict, key=lambda n: n[sort_arg_type], reverse=True)
        else:
            return sorted(notes_dict, key=lambda n: n[sort_arg_type], reverse=False)
    current_notes = sort_notes(notes_new, sort_arg, order_arg)

    author = request.args.get("author")
    limit = request.args.get("limit")
    if limit is None:
        limit = 10
    value_limit = get_int(limit)
    if value_limit is None:
        return jsonify(error="limit must be an integer"), 400
    if value_limit < 1 or value_limit > 100:
        return jsonify(error="limit must be between 1 and 100"), 400
    offset = request.args.get("offset")
    if offset is None:
        offset = 0
    value_offset = get_int(offset)
    if value_offset is None:
        return jsonify(error="offset must be an integer"), 400
    if value_offset < 0:
        return jsonify(error="offset must be >= 0"), 400
    result = current_notes
    if author is not None:
        result = [n for n in current_notes if n["author"] == author]
    result = result[value_offset:value_offset + value_limit]
    return jsonify(result), 200

@app.post("/notes")
def create_note():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data:
        return jsonify(error="field 'data' (dict) is required"), 400
    if not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400
    if not isinstance(data.get("author"), str) or not data["author"].strip():
        return jsonify(error="field 'author' (non-empty string) is required"), 400
    note = {
        "id": next(note_ids),
        "text": data["text"].strip(),
        "author": data["author"].strip(),
        "likes": 0,
    }
    write_to_json(note)
    return jsonify(note), 201

@app.put("/notes/<int:note_id>")
def update_note(note_id):
    notes_new = read_json()
    idx = get_index(notes_new, "id", note_id)
    if idx is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data:
        return jsonify(error="field 'data' (dict) is required"), 400
    if not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400
    if not isinstance(data.get("author"), str) or not data["author"].strip():
        return jsonify(error="field 'author' (non-empty string) is required"), 400
    notes_new[idx]["text"] = data["text"].strip()
    notes_new[idx]["author"] = data["author"].strip()
    update_all_json(notes_new)
    return jsonify(notes_new[idx]), 200

@app.patch("/notes/<int:note_id>")
def update_text_note(note_id):
    notes_new = read_json()
    idx = get_index(notes_new, "id", note_id)
    if idx is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data:
        return jsonify(error="field 'data' (dict) is required"), 400
    if not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400
    notes_new[idx]["text"] = data["text"].strip()
    update_all_json(notes_new)
    return jsonify(notes_new[idx]), 200

@app.get("/notes/<int:note_id>")
def get_note(note_id):
    notes_new = read_json()
    note = find_note(note_id, notes_new)
    if note is None:
        abort(404)
    return jsonify(note)

@app.get("/authors")
def statistic_by_author():
    notes_new = read_json()
    stats = []
    sort_notes_by_name = sorted(notes_new, key=lambda n: n["author"])
    for i in range(len(sort_notes_by_name)):
        if i == 0 or sort_notes_by_name[i]["author"] != sort_notes_by_name[i-1]["author"]:
            statistic = {"author": sort_notes_by_name[i]["author"], "notes": 1, "likes": sort_notes_by_name[i]["likes"]}
            stats.append(statistic)
        else:
            stats[-1]["likes"] += sort_notes_by_name[i]["likes"]
            stats[-1]["notes"] += 1
    return jsonify(stats), 200

@app.post("/notes/<int:note_id>/like")
def add_like(note_id):
    notes_new = read_json()
    idx = get_index(notes_new, "id", note_id)
    if idx is None:
        abort(404)
    notes_new[idx]["likes"] += 1
    update_all_json(notes_new)
    return jsonify(notes_new[idx]), 200

@app.delete("/notes")
def delete_notes_by_author():
    notes_new = read_json()
    author = request.args.get("author")

    if author is None or not isinstance(author, str) or not author.strip():
        return jsonify(error= "author must be a string"), 400

    del_count = 0
    list_for_remove = []
    for i in range(len(notes_new)):
        if notes_new[i]["author"] == author.strip():
            list_for_remove.append(notes_new[i])
            del_count += 1
    for i in list_for_remove:
        notes_new.remove(i)
    update_all_json(notes_new)
    return jsonify({"deleted": del_count})

@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    notes_new = read_json()
    note = find_note(note_id, notes_new)
    if note is None:
        abort(404)
    notes_new.remove(note)
    update_all_json(notes_new)
    return "", 204

@app.errorhandler(404)
def not_found(error):
    return jsonify(error="not found"), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error="method not allowed"), 405

if __name__ == "__main__":
    app.run(debug=True)