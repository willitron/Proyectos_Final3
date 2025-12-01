from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Rol, Permiso
from utils.decorators import permiso_requerido

rol_bp = Blueprint('rol', __name__, url_prefix='/roles')

@rol_bp.route('/')
@login_required
@permiso_requerido('ver_roles')
def index():
    roles = Rol.query.order_by(Rol.nombre).all()
    # Contar usuarios por cada rol
    for rol in roles:
        rol.usuarios_count = len(rol.usuarios)
    return render_template('rol/index.html', roles=roles)

@rol_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_rol')
def crear():
    if request.method == 'POST':
        try:
            rol = Rol(
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion')
            )
            
            # Asignar permisos
            permiso_ids = request.form.getlist('permisos')
            for permiso_id in permiso_ids:
                permiso = Permiso.query.get(int(permiso_id))
                if permiso:
                    rol.permisos.append(permiso)
            
            db.session.add(rol)
            db.session.commit()
            flash('Rol creado exitosamente.', 'success')
            return redirect(url_for('rol.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear rol: {str(e)}', 'danger')
    
    permisos = Permiso.query.order_by(Permiso.nombre).all()
    return render_template('rol/crear.html', permisos=permisos)

@rol_bp.route('/<int:id>')
@login_required
@permiso_requerido('ver_roles')
def detalle(id):
    rol = Rol.query.get_or_404(id)
    return render_template('rol/detalle.html', rol=rol)

@rol_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_rol')
def editar(id):
    rol = Rol.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            rol.nombre = request.form['nombre']
            rol.descripcion = request.form.get('descripcion')
            
            # Actualizar permisos
            rol.permisos.clear()
            permiso_ids = request.form.getlist('permisos')
            for permiso_id in permiso_ids:
                permiso = Permiso.query.get(int(permiso_id))
                if permiso:
                    rol.permisos.append(permiso)
            
            db.session.commit()
            flash('Rol actualizado exitosamente.', 'success')
            return redirect(url_for('rol.detalle', id=rol.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar rol: {str(e)}', 'danger')
    
    permisos = Permiso.query.order_by(Permiso.nombre).all()
    return render_template('rol/editar.html', rol=rol, permisos=permisos)

@rol_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_rol')
def eliminar(id):
    rol = Rol.query.get_or_404(id)
    
    try:
        db.session.delete(rol)
        db.session.commit()
        flash('Rol eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar rol: {str(e)}', 'danger')
    
    return redirect(url_for('rol.index'))