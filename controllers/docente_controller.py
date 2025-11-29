from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Docente, Persona
from utils.decorators import permiso_requerido
from datetime import datetime

docente_bp = Blueprint('docente', __name__, url_prefix='/docentes')

@docente_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    docentes = Docente.query.join(Persona).order_by(Persona.apellido_paterno).paginate(page=page, per_page=10, error_out=False)
    return render_template('docente/index.html', docentes=docentes)

@docente_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_docente')
def crear():
    if request.method == 'POST':
        try:
            docente = Docente(
                persona_id=int(request.form['persona_id']),
                codigo_docente=request.form['codigo_docente'],
                grado_academico=request.form.get('grado_academico'),
                fecha_ingreso=datetime.strptime(request.form['fecha_ingreso'], '%Y-%m-%d').date() if request.form.get('fecha_ingreso') else None,
                fecha_nacimiento=datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date() if request.form.get('fecha_nacimiento') else None,
                titulo_universitario=request.form.get('titulo_universitario'),
                activo=bool(request.form.get('activo'))
            )
            db.session.add(docente)
            db.session.commit()
            flash('Docente creado exitosamente.', 'success')
            return redirect(url_for('docente.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear docente: {str(e)}', 'danger')
    
    personas = Persona.query.outerjoin(Docente).filter(Docente.id == None).all()
    return render_template('docente/crear.html', personas=personas)

@docente_bp.route('/<int:id>')
@login_required
def detalle(id):
    docente = Docente.query.get_or_404(id)
    return render_template('docente/detalle.html', docente=docente)

@docente_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_docente')
def editar(id):
    docente = Docente.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            docente.codigo_docente = request.form['codigo_docente']
            docente.grado_academico = request.form.get('grado_academico')
            docente.fecha_ingreso = datetime.strptime(request.form['fecha_ingreso'], '%Y-%m-%d').date() if request.form.get('fecha_ingreso') else None
            docente.fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date() if request.form.get('fecha_nacimiento') else None
            docente.titulo_universitario = request.form.get('titulo_universitario')
            docente.activo = bool(request.form.get('activo'))
            
            db.session.commit()
            flash('Docente actualizado exitosamente.', 'success')
            return redirect(url_for('docente.detalle', id=docente.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar docente: {str(e)}', 'danger')
    
    return render_template('docente/editar.html', docente=docente)

@docente_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_docente')
def eliminar(id):
    docente = Docente.query.get_or_404(id)
    
    try:
        db.session.delete(docente)
        db.session.commit()
        flash('Docente eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar docente: {str(e)}', 'danger')
    
    return redirect(url_for('docente.index'))