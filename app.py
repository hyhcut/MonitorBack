from flask import Flask, request
from flask_cors import *
# from flask_login import login_user, logout_user, login_required
from ext import db
from models import *
import util.Ajax as Ajax
import datetime
from Link import Link

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
        return Ajax.error("用户不存在")
    if user.check_password(password):
        # login_user(user)
        user.last_time = datetime.datetime.now()
        db.session.commit()
        return Ajax.success({
            'message': "登陆成功",
            'power': user.power_id
        })
    else:
        return Ajax.error("密码错误")


# @app.route('/logout', methods=['POST'])
# def logout():
#     logout_user()
#     return jsonify(Ajax.success("注销成功"))
@app.route('/user/get', methods=['POST'])
def user_get():
    id = request.json.get('id')
    user = User.query.get(id)
    return Ajax.success(user.list_show())


@app.route('/user/list', methods=['POST'])
def user_list():
    result = []
    user_list = User.query.filter(User.id != 1).all()
    for user in user_list:
        result.append(user.list_show())
    return Ajax.success(result)


@app.route('/user/add', methods=['POST'])
def user_add():
    user = User(request.json)
    db.session.add(user)
    db.session.commit()
    return Ajax.success("成功")


@app.route('/user/update', methods=['POST'])
def user_update():
    dict = request.json
    user = User.query.get(dict.get('id'))
    if user.check_password(dict.get('old_password')):
        if user.username != dict.get("username") and User.query.filter(User.username == dict.get('username')).all():
            return Ajax.error('用户名已存在')
        else:
            if dict.get('new_password'):
                user.set_password(dict.get('new_password'))
            print(type(dict))
            user.__init__(dict)
            db.session.commit()
            return Ajax.success('修改成功')
    else:
        return Ajax.error('原密码错误')


@app.route('/user/delete', methods=['POST'])
def user_delete():
    id = request.json.get('id')
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return Ajax.success("成功")


@app.route('/power/list', methods=['POST'])
def power_list():
    result = []
    power_list = DictPower.query.all()
    for power in power_list:
        result.append(power.select_show())
    return Ajax.success(result)


@app.route('/server/type/list', methods=['POST'])
def server_type_list():
    result = []
    list = DictServerType.query.all()
    for server_type in list:
        result.append(server_type.select_show())
    return Ajax.success(result)


@app.route('/manual', methods=['POST'])
def manual():
    server = request.json
    link = Link(server.get("name"), server.get("address"), server.get("username"), server.get("password"), None)
    if link.test():
        return Ajax.success(link.manual())
    else:
        return Ajax.error("服务器无法连接")


if __name__ == '__main__':
    app.run()
