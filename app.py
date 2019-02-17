from flask import Flask, request
from flask_cors import *
# from flask_login import login_user, logout_user, login_required
from ext import db
from models import *
import util.Ajax as Ajax
import datetime
from Windows import Link
from Linux import Linux

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
    type = server.get('server_type')
    if type == 1:
        link = Link(server.get("name"), server.get("address"), server.get("username"), server.get("password"), None)
        if link.test():
            return Ajax.success(link.manual())
        else:
            return Ajax.error("服务器无法连接")
    elif type == 2:
        link = Linux(server.get('name'), server.get('address'), server.get('username'), server.get('password'))
        if link.connect():
            return Ajax.success(link.manual())
        else:
            return Ajax.error("连接服务器超时")


@app.route('/server/list', methods=['POST'])
def server_list():
    result = []
    server_list = Server.query.all()
    for server in server_list:
        result.append(server.list_show())
    return Ajax.success(result)


@app.route('/server/get', methods=['POST'])
def server_get():
    server = Server.query.get(int(request.json.get('id')))
    return Ajax.success(server.list_show())


@app.route('/server/add', methods=['POST'])
def server_add():
    server = Server(request.json)
    db.session.add(server)
    db.session.commit()
    return Ajax.success("服务器创建成功")


@app.route('/server/delete', methods=['POST'])
def server_delete():
    server = Server.query.get(int(request.json.get('id')))
    db.session.delete(server)
    db.session.commit()
    return Ajax.success("删除成功")


@app.route('/server/update', methods=['POST'])
def server_update():
    dict = request.json
    server = Server.query.get(int(dict.get('id')))
    if server.name != dict.get("name") and Server.query.filter(Server.name == dict.get('name')).all():
        return Ajax.error('服务器名称已存在')
    else:
        server.__init__(dict)
        db.session.commit()
        return Ajax.success('修改成功')


if __name__ == '__main__':
    app.run()
