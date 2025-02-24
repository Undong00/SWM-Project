import os
import certifi
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
import hashlib

app = Flask(__name__)

ca = certifi.where()
client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.g85ftsp.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


# api
@app.route('/')
def home():
    return render_template('index.html')


# sign-up apis

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        id = request.form['id']
        nickname = request.form['nickname']
        password = request.form['password']

        #  아이디 중복 검사
        if db.pjs.find_one({'id': id}):
           return jsonify({'message': '이미 존재하는 아이디입니다.'})

        # 랜덤 솔트 값 생성
        salt = os.urandom(16)

        # 솔트랑 비번 합쳐서 해싱/ Encode로 bytes obj 만들어서 해싱하고 다시 16진수 스트링으로 변환(hexdigest())
        hashed_password = hashlib.sha256(password.encode() + salt).hexdigest()

        doc = {
            'id': id, 'nickname': nickname, 'salt': salt, 'password': hashed_password
            }
        db.pjs.insert_one(doc)
        
        # return redirect(url_for('home'))
        return jsonify({'message' :'가입 완료'})
    else:
        return render_template('join.html')



# todo apis
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
