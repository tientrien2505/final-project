from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField

class CameraForm(FlaskForm ):
    camera_name = StringField('Camera name')
    ip_address = StringField('IP Address')
    code = StringField('CODE')
    submit = SubmitField('Add')

class DepartmentForm(FlaskForm):
    department_name = StringField('Department name')
    submit = SubmitField('Add')


class LockForm(FlaskForm):
    lock_name = StringField('Lock name')
    code = StringField('Code')
    info = StringField('Info')
    submit = SubmitField('Add')


class EmployeeForm(FlaskForm):
    username = StringField('Username')
    fullname = StringField('Fullname')
    code = StringField('Code')
    department_id = SelectField('Department', choices=[], coerce=int)
    # form: camera_id_1,camera_id_2,...
    locks = HiddenField('lock')
    submit = SubmitField('Add')