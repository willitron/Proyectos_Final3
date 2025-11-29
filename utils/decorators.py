from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user

def login_required_with_message(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def permiso_requerido(permiso):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión.', 'warning')
                return redirect(url_for('auth.login'))
            
            if not current_user.tiene_permiso(permiso):
                flash('No tienes permisos para realizar esta acción.', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def rol_requerido(rol):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión.', 'warning')
                return redirect(url_for('auth.login'))
            
            if not current_user.tiene_rol(rol):
                flash('No tienes el rol necesario para acceder.', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator