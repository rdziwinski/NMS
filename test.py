import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '123456790'

#database = db.session.query(Host).all()
database = Host().show_all()
print(database)
