import certifi
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
ca = certifi.where()
client = MongoClient(
    'mongodb+srv://sparta:sparta@cluster0.1dpm6q3.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/todo", methods=["POST"])
def todo_post():
    todo_receive = request.form['todo_give']
    doc = {
        'todo': todo_receive
    }
    db.todolist.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})




@app.route("/todo", methods=["GET"])
def todo_get():
    comments = list(db.todolist.find())
    comments = [{**comment, **{"_id": str(comment["_id"])}}
                for comment in comments]
    return jsonify({'result': comments})


@app.route("/todo", methods=["DELETE"])
def todo_delete():
    delete_receive = request.form["id"]
    db.todolist.delete_one({'_id': ObjectId(delete_receive)})
    return jsonify({'msg': "삭제 완료!"})

@app.route("/todo", methods=["PUT"])
def todo_update():
    id_receive = request.form["id"]
    new_todo = request.form["new_todo"]
    db.todolist.update_one({'_id': ObjectId(id_receive)}, {"$set": {"todo": new_todo}})
    return jsonify({'msg': "수정 완료!"})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
