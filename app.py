from flask import Flask, request, jsonify
from flask_cors import *
# from flask_login import login_user, logout_user, login_required
from ext import db
from models import *
import util.Ajax as Ajax
import datetime

app = Flask(__name__)
app.config.from_object("config")
CORS(app, support_credentails=True)
db.init_app(app)


# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(id)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(Ajax.error("用户不存在"))
    if user.check_password(password):
        # login_user(user)
        user.last_time = datetime.datetime.now()
        db.session.commit()
        return jsonify(Ajax.success({
            'message': "登陆成功",
            'power': user.power_id
        }))
    else:
        return jsonify(Ajax.error("密码错误"))


# @app.route('/logout', methods=['POST'])
# def logout():
#     logout_user()
#     return jsonify(Ajax.success("注销成功"))


@app.route('/user/list', methods=['POST'])
def user_list():
    result = []
    user_list= User.query.all()
    # user_list = User.query.filter(User.id != 1).all()
    for user in user_list:
        result.append(user.list_show())
    return jsonify(Ajax.success(result))


if __name__ == '__main__':
    app.run()
