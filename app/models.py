from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    fullname = db.Column(db.String(140))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_password(self, pass_str):
        self.password_hash = generate_password_hash(pass_str)

    def check_password(self, pass_str):
        return check_password_hash(self.password_hash, pass_str)


class Camera(db.Model):
    __tablename__ = 'camera'
    camera_id = db.Column(db.Integer, primary_key=True)
    camera_name = db.Column(db.String(50), unique=True)
    code = db.Column(db.String(20), unique=True)
    ip_address = db.Column(db.String(20), unique=True)
    rtsp_transport = db.Column(db.String(5), default='tcp')

    def to_dict(self, *attributes):
        res = {
            'camera_id': self.camera_id,
            'camera_name': self.camera_name,
            'ip_address': self.ip_address,
            'code': self.code
        }
        return res
    @classmethod
    def get_camera(cls, camera_id=None):
        if camera_id is None:
            res = [camera.to_dict() for camera in Camera.query.all()]
        else:
            camera = Camera.query.filter_by(camera_id=camera_id).first()
            if camera is not None:
                res = camera.to_dict()
            else:
                res = {}
        return res

class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    fullname = db.Column(db.String(100), unique=True)
    code = db.Column(db.String(20), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    # form: camera_id_1,camera_id_2,...
    locks = db.Column(db.String(500))

class Image(db.Model):
    __tablename__ = 'image'
    image_id = db.Column(db.Integer, primary_key=True)
    # emp_id + timestamp
    name = db.Column(db.String(30), unique=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))

class Lock(db.Model):
    __tablename__ = 'lock'
    lock_id = db.Column(db.Integer, primary_key=True)
    lock_name = db.Column(db.String(30), unique=True)
    code = db.Column(db.String(20), unique=True)
    # info either pin or controller ip
    info = db.Column(db.String(30), unique=True)

    def to_dict(self):
        res = {
            'lock_id': self.lock_id,
            'lock_name': self.lock_name,
            'info': self.info,
            'code': self.code
        }
        return res

    @classmethod
    def get_lock(cls, lock_id=None):
        if lock_id is None:
            res = [lock.to_dict() for lock in Lock.query.all()]
        else:
            lock = Lock.query.filter_by(lock_id=lock_id).first()
            if lock is not None:
                res = lock.to_dict()
            else:
                res = {}
        return res
    
class CameraLock(db.Model):
    __tablename__ = 'camera_lock'
    camera_lock_id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.camera_id'))
    lock_id = db.Column(db.Integer, db.ForeignKey('lock.lock_id'))