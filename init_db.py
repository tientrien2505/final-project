from app import db, app
from app.models import User

app.app_context().push()

def create_super_user():
    super_user = User(username='root')
    super_user.set_password('basmnjnszk465')
    db.session.add(super_user)
    db.session.commit()

if __name__ == '__main__':
    create_super_user()