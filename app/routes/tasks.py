from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task, User
from flask_login import login_required, current_user

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).count()
    users = User.query.count()
    return render_template('dashboard.html',tasks=tasks, users=users)

@tasks_bp.route('/tasks')
@login_required
def view_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html',tasks=tasks)

@tasks_bp.route('/add',methods=["POST"])
@login_required
def add_tasks():
   title = request.form.get('title')
   if title:
       new_task = Task(title=title, status="Pending", user_id=current_user.id)
       db.session.add(new_task)
       db.session.commit()
       flash('Task Added Successfully','success')

   return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>',methods=['POST'])
@login_required
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == "Pending":
            task.status = "Working"
        elif task.status == "Working":
            task.status = "Done"
        else:
            task.status = "Pending"
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/delete/<int:tid>', methods=['GET'])
def delete_task(tid):
    Task.query.filter_by(id=tid).delete()
    db.session.commit()
    flash('Task deleted Successfully!','success')
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear/',methods=['POST'])
@login_required
def clear_task():
    Task.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Clear All Tasks','success')
    return redirect(url_for('tasks.view_tasks'))
