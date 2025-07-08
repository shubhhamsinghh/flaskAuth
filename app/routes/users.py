from flask import Flask, Blueprint, redirect, request, url_for, session, flash, render_template, jsonify
from flask_login import login_required, current_user
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

users_bp = Blueprint('users',__name__)

@users_bp.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html',users=users)

@users_bp.route('/users/users-update/<int:userId>',methods=['GET'])
@login_required
def updateStatus(userId):
    if userId != 1 and current_user.is_admin == 1:
        user = User.query.get_or_404(userId)
        user.status = 0 if user.status == 1 else 1
        db.session.commit()
        return jsonify({'success': True, 'message': 'User status updated!'})
    else:
        return jsonify({'success': False, 'message': 'Access denied!'})

@users_bp.route('/users/is-admin/<int:userId>',methods=['GET'])
@login_required
def is_admin(userId):
    if userId != 1 and current_user.is_admin == 1:
        user = User.query.get_or_404(userId)
        user.is_admin = 0 if user.is_admin == 1 else 1
        db.session.commit()
        return jsonify({'success': True, 'message': 'User privilege updated!'})
    else:
        return jsonify({'success': False, 'message': 'Access denied!'})
    
@users_bp.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
    if request.method == 'POST':
        if request.form.get('new_pass') == request.form.get('conf_pass'):
            passwrd = request.form.get('new_pass')
            user = User.query.get_or_404(current_user.id)
            user.password = generate_password_hash(passwrd)
            db.session.commit()
            flash('Password changs successfully!','success')
            return redirect(url_for('users.change_password'))
        else:
            flash('Password mismatch. Try again!','error')
            return redirect(url_for('users.change_password'))
    else:
        return render_template('change-password.html')

