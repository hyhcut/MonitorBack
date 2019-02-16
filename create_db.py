from app import db, app
from models import *

db.init_app(app)
db.create_all(app=app)