from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Persona
from utils.decorators import permiso_requerido
from datetime import datetime

persona_bp = Blueprint('persona', __name__, url_prefix='/personas')

@persona_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    personas = Persona.query.order_by(Persona.apellido_paterno, Persona.nombre).paginate(page=page, per_page=10, error_out=False)
    return render_template('persona/index.html', personas=personas)

@persona_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_persona')
def crear():
    if request.method == 'POST':
        try:
            persona = Persona(
                tipo_documento=request.form['tipo_documento'],
                nro_documento=request.form['nro_documento'],
                nombre=request.form['nombre'],
                apellido_paterno=request.form['apellido_paterno'],
                apellido_materno=request.form.get('apellido_materno'),
                fecha_nacimiento=datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date() if request.form.get('fecha_nacimiento') else None,
                sexo=request.form.get('sexo'),
                lugar_nacimiento=request.form.get('lugar_nacimiento'),
                direccion=request.form.get('direccion'),
                telefono=request.form.get('telefono'),
                email=request.form.get('email')
            )
            db.session.add(persona)
            db.session.commit()
            flash('Persona creada exitosamente.', 'success')
            return redirect(url_for('persona.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear persona: {str(e)}', 'danger')
    
    return render_template('persona/crear.html')

@persona_bp.route('/<int:id>')
@login_required
def detalle(id):
    persona = Persona.query.get_or_404(id)
    return render_template('persona/detalle.html', persona=persona)

@persona_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_persona')
def editar(id):
    persona = Persona.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            persona.tipo_documento = request.form['tipo_documento']
            persona.nro_documento = request.form['nro_documento']
            persona.nombre = request.form['nombre']
            persona.apellido_paterno = request.form['apellido_paterno']
            persona.apellido_materno = request.form.get('apellido_materno')
            persona.fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date() if request.form.get('fecha_nacimiento') else None
            persona.sexo = request.form.get('sexo')
            persona.lugar_nacimiento = request.form.get('lugar_nacimiento')
            persona.direccion = request.form.get('direccion')
            persona.telefono = request.form.get('telefono')
            persona.email = request.form.get('email')
            
            db.session.commit()
            flash('Persona actualizada exitosamente.', 'success')
            return redirect(url_for('persona.detalle', id=persona.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar persona: {str(e)}', 'danger')
    
    return render_template('persona/editar.html', persona=persona)

@persona_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_persona')
def eliminar(id):
    persona = Persona.query.get_or_404(id)
    
    try:
        db.session.delete(persona)
        db.session.commit()
        flash('Persona eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar persona: {str(e)}', 'danger')
    
    return redirect(url_for('persona.index'))