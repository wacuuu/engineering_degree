from flask import Flask
from flask import request
from flask import jsonify
from db_interfaces import db_operations

db_operations.setup_connection()
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, Flask!'


@app.route('/api/create/', methods=["POST"])
def write():
    data = request.get_json()
    db_operations.write(data)
    return "fine\n"


@app.route('/api/read/', methods=["GET"])
def read():
    request_dict = request.get_json()
    if request_dict is not None:
        tmp = []
        for key in request_dict.keys():
            if len(request_dict[key]) == 0:
                tmp.append(key)
        for i in tmp:
            request_dict.pop(i, "")
        result = db_operations.read(request_dict)
    else:
        result = db_operations.read()
    for element in result:
        element["date"] = str(element["date"])
    return jsonify(result)


@app.route('/api/update/', methods=["POST"])
def update():
    data = request.get_json()
    db_operations.update(data)
    return "fine\n"


@app.route('/api/delete/', methods=["POST"])
def delete():
    data = request.get_json()
    db_operations.delete(data)
    return "fine\n"

if __name__ == '__main__':
    app.run()
