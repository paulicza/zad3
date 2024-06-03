from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import TaskForm
from app.models import Task
from app import db
from flask_login import login_required, current_user

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    return render_template('index.html')

@tasks_bp.route('/tasks')
@login_required
def list_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('list_tasks.html', tasks=tasks)

@tasks_bp.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data, 
            description=form.description.data, 
            deadline=form.deadline.data, 
            user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks.list_tasks'))
    return render_template('create_task.html', form=form)

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        return redirect(url_for('tasks.list_tasks'))
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.deadline = form.deadline.data
        db.session.commit()
        return redirect(url_for('tasks.list_tasks'))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.deadline.data = task.deadline
    return render_template('edit_task.html', form=form)

@tasks_bp.route('/open/<int:task_id>/open')
@login_required
def open_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You are not authorized to delete this task.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    return render_template('open_task.html', task=task)

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash('You are not authorized to delete this task.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted.', 'success')
    return redirect(url_for('tasks.list_tasks'))

@tasks_bp.route('/all_tasks')
@login_required
def all_tasks():
    if current_user.role == 'admin':
        tasks = Task.query.all()
        return render_template('all_tasks.html', tasks=tasks)
    else:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
