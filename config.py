import os
# 项目根目录
root_path = os.path.abspath(os.path.dirname(__file__))
# 数据库配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://monitor:hyh282038@127.0.0.1:3306/Monitor'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'hyh282038'