from flask import render_template, Response, request, redirect, url_for, jsonify
from app import app, db
from app.models import *
from app.forms import *
from app.util.camera_util import gen_frames

@app.route('/api/delete_camera', methods=['POST'])
def delete_camera():
    res = {
        'success': True
    }
    try:
        camera_id = request.values['camera_id']
        camera = Camera.query.filter_by(camera_id=camera_id).first()
        db.session.delete(camera)
        db.session.commit()
    except:
        res['success'] = False
    return jsonify(res)


@app.route('/api/delete_department', methods=['POST'])
def delete_department():
    res = {
        'success': True
    }
    try:
        department_id = request.values['department_id']
        department = Department.query.filter_by(department_id=department_id).first()
        db.session.delete(department)
        db.session.commit()
    except:
        res['success'] = False
    return jsonify(res)


@app.route('/api/delete_lock', methods=['POST'])
def delete_lock():
    res = {
        'success': True
    }
    try:
        lock_id = request.values['lock_id']
        lock = Lock.query.filter_by(lock_id=lock_id).first()
        db.session.delete(lock)
        db.session.commit()
    except:
        res['success'] = False
    return jsonify(res)


@app.route('/api/camera')
def get_camera():
    res = Camera.get_camera()
    return jsonify(res)


@app.route('/api/lock')
def get_lock():
    res = Lock.get_lock()
    return jsonify(res)