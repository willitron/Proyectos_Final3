from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Usuario, Persona, Estudiante, Docente, Rol
from utils.decorators import permiso_requerido

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_bp.route('/')
@login_required
@permiso_requerido('ver_usuarios')
def index():
    page = request.args.get('page', 1, type=int)
    usuarios = Usuario.query.order_by(Usuario.username).paginate(page=page, per_page=10, error_out=False)
    return render_template('usuario/index.html', usuarios=usuarios)

@usuario_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_usuario')
def crear():
    if request.method == 'POST':
        try:
            usuario = Usuario(
                username=request.form['username'],
                email=request.form.get('email'),
                persona_id=int(request.form['persona_id']) if request.form.get('persona_id') else None,
                estudiante_id=int(request.form['estudiante_id']) if request.form.get('estudiante_id') else None,
                docente_id=int(request.form['docente_id']) if request.form.get('docente_id') else None,
                activo=bool(request.form.get('activo'))
            )
            usuario.set_password(request.form['password'])
            
            rol_ids = request.form.getlist('roles')
            for rol_id in rol_ids:
                rol = Rol.query.get(int(rol_id))
                if rol:
                    usuario.roles.append(rol)
            
            db.session.add(usuario)
            db.session.commit()
            flash('Usuario creado exitosamente.', 'success')
            return redirect(url_for('usuario.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear usuario: {str(e)}', 'danger')
    
    personas = Persona.query.all()
    estudiantes = Estudiante.query.all()
    docentes = Docente.query.all()
    roles = Rol.query.all()
    return render_template('usuario/crear.html', personas=personas, estudiantes=estudiantes, docentes=docentes, roles=roles)

@usuario_bp.route('/<int:id>')
@login_required
@permiso_requerido('ver_usuarios')
def detalle(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template('usuario/detalle.html', usuario=usuario)

@usuario_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_usuario')
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            usuario.username = request.form['username']
            usuario.email = request.form.get('email')
            usuario.persona_id = int(request.form['persona_id']) if request.form.get('persona_id') else None
            usuario.estudiante_id = int(request.form['estudiante_id']) if request.form.get('estudiante_id') else None
            usuario.docente_id = int(request.form['docente_id']) if request.form.get('docente_id') else None
            usuario.activo = bool(request.form.get('activo'))
            
            if request.form.get('password'):
                usuario.set_password(request.form['password'])
            
            usuario.roles.clear()
            rol_ids = request.form.getlist('roles')
            for rol_id in rol_ids:
                rol = Rol.query.get(int(rol_id))
                if rol:
                    usuario.roles.append(rol)
            
            db.session.commit()
            flash('Usuario actualizado exitosamente.', 'success')
            return redirect(url_for('usuario.detalle', id=usuario.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar usuario: {str(e)}', 'danger')
    
    personas = Persona.query.all()
    estudiantes = Estudiante.query.all()
    docentes = Docente.query.all()
    roles = Rol.query.all()
    return render_template('usuario/editar.html', usuario=usuario, personas=personas, estudiantes=estudiantes, docentes=docentes, roles=roles)

@usuario_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_usuario')
def eliminar(id):
    usuario = Usuario.query.get_or_404(id)
    
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar usuario: {str(e)}', 'danger')
    
    return redirect(url_for('usuario.index'))