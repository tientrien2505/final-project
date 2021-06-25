from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/truongdt/projects/faceid/final-project/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'aflskdjf;klqjwefkjl;akjdfl;kajsd;lfjlak;sdjfkl;ajeklfjlkdjflkjdklj'
bootstrap = Bootstrap()
bootstrap.init_app(app)
csrf = CSRFProtect()
csrf.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
db.create_all()
migrate = Migrate()
migrate.init_app(app, db)

from app.models import *
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

from app.routes import *
from app.api import *