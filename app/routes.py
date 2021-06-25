from flask import render_template, Response, request, redirect, url_for
from app import app, db
from app.models import *
from app.forms import *
from app.util.camera_util import gen_frames

import time


@app.route('/')
def index():
    return '<h1>welcome to NMS FaceID System</h1>'


@app.route('/video_feed')
def video_feed():
    url = request.values['url']
    rtsp_transport = request.values['rtsp_transport'] if 'rtsp_transport' in request.values else 'tcp'
    return Response(gen_frames(url, rtsp_transport), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cameras', methods=['POST', 'GET'])
def cameras():
    form = CameraForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            camera = Camera()
            camera.camera_name = form.camera_name.data
            camera.ip_address = form.ip_address.data
            camera.code = form.code.data
            try:
                db.session.add(camera)
                db.session.commit()
            except:
                print('process camera existed')
        return redirect(url_for('cameras'))
    camera_list = Camera.query.all()
    print(camera_list)
    return render_template('cameras.html', form=form, title='Cameras', breadcrumb_item_1='Cameras', camera_list=camera_list, active_cameras='active')


@app.route('/cameras/<int:camera_id>')
def camera(camera_id):
    """
    display camera detail
    """
    return '<h1>hello</h1>' + str(camera_id)

@app.route('/departments', methods=['POST', 'GET'])
def departments():
    """
    show all departments
    :return:
    """
    form = DepartmentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            department = Department()
            department.name = form.department_name.data
            try:
                db.session.add(department)
                db.session.commit()
            except:
                print('process department existed')
        return redirect(url_for('departments'))
    department_list = Department.query.all()
    return render_template('departments.html', form=form, title='Departments', breadcrumb_item_1='Departments', department_list=department_list, active_departments='active')

@app.route('/departments/<int:department_id>')
def department(department_id):
    """
    if department_id == 0 then add new
    else show department and allow edit
    :param department_id:
    :return:
    """
    pass

@app.route('/employees', methods=['POST', 'GET'])
def employees():
    """
    show all employees
    :return:
    """
    form = EmployeeForm()
    departments = Department.query.all()
    form.department_id.choices = [(department.department_id, department.name) for department in departments]
    if request.method == 'POST':
        if form.validate_on_submit():
            employee = Employee()
            employee.username = form.username.data
            employee.fullname = form.fullname.data
            employee.code = form.code.data
            employee.department_id = form.department_id.data
            employee.locks = form.locks.data
            try:
                db.session.add(employee)
                db.session.commit()
            except:
                print('process employee existed')
        return redirect(url_for('employees'))
    employee_list = Employee.query.all()
    return render_template('employees.html', form=form, title='Employees', breadcrumb_item_1='Employees', employee_list=employee_list, active_employees='active')

@app.route('/employees/<int:employee_id>')
def employee(employee_id):
    """
    if employee_id == 0 then add new
    else show information of employee and allow edit
    :param employee_id:
    :return:
    """
    return render_template('photo.html')


@app.route('/locks', methods=['POST', 'GET'])
def locks():
    form = LockForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            lock = Lock()
            lock.lock_name = form.lock_name.data
            lock.code = form.code.data
            lock.info = form.info.data
            try:
                db.session.add(lock)
                db.session.commit()
            except:
                print('process lock existed')
        return redirect(url_for('locks'))
    lock_list = Lock.query.all()
    return render_template('locks.html', form=form, title='Locks', breadcrumb_item_1='Locks', lock_list=lock_list, active_locks='active')