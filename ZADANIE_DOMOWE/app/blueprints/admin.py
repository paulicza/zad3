from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Task, User
from functools import wraps
from flask import abort

admin_bp = Blueprint('admin', __name__)

def role_required(role): 
    def decorator(func): 
        @wraps(func) 
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != 'admin': 
                abort(403) 
            return func(*args, **kwargs) 
        return decorated_view
    return decorator

@admin_bp.route('/admin')
@login_required
@role_required('admin')
def admin():
    return f'Hello Admin {current_user.username}!'
