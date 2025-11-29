from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Inscripcion, Estudiante, Carrera
from utils.decorators import permiso_requerido

inscripcion_bp = Blueprint('inscripcion', __name__, url_prefix='/inscripciones')

@inscripcion_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    inscripciones = Inscripcion.query.order_by(Inscripcion.gestion.desc(), Inscripcion.fecha_inscripcion.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('inscripcion/index.html', inscripciones=inscripciones)

@inscripcion_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_inscripcion')
def crear():
    if request.method == 'POST':
        try:
            inscripcion = Inscripcion(
                estudiante_id=int(request.form['estudiante_id']),
                carrera_id=int(request.form['carrera_id']),
                gestion=int(request.form['gestion']),
                periodo=request.form['periodo'],
                estado=request.form.get('estado', 'Matriculado'),
                metodo_ingreso=request.form.get('metodo_ingreso', 'Regular')
            )
            db.session.add(inscripcion)
            db.session.commit()
            flash('Inscripción creada exitosamente.', 'success')
            return redirect(url_for('inscripcion.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear inscripción: {str(e)}', 'danger')
    
    estudiantes = Estudiante.query.filter_by(activo=True).all()
    carreras = Carrera.query.filter_by(activo=True).all()
    return render_template('inscripcion/crear.html', estudiantes=estudiantes, carreras=carreras)

@inscripcion_bp.route('/<int:id>')
@login_required
def detalle(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    return render_template('inscripcion/detalle.html', inscripcion=inscripcion)

@inscripcion_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_inscripcion')
def editar(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            inscripcion.estudiante_id = int(request.form['estudiante_id'])
            inscripcion.carrera_id = int(request.form['carrera_id'])
            inscripcion.gestion = int(request.form['gestion'])
            inscripcion.periodo = request.form['periodo']
            inscripcion.estado = request.form.get('estado', 'Matriculado')
            inscripcion.metodo_ingreso = request.form.get('metodo_ingreso', 'Regular')
            
            db.session.commit()
            flash('Inscripción actualizada exitosamente.', 'success')
            return redirect(url_for('inscripcion.detalle', id=inscripcion.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar inscripción: {str(e)}', 'danger')
    
    estudiantes = Estudiante.query.filter_by(activo=True).all()
    carreras = Carrera.query.filter_by(activo=True).all()
    return render_template('inscripcion/editar.html', inscripcion=inscripcion, estudiantes=estudiantes, carreras=carreras)

@inscripcion_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_inscripcion')
def eliminar(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    
    try:
        db.session.delete(inscripcion)
        db.session.commit()
        flash('Inscripción eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar inscripción: {str(e)}', 'danger')
    
    return redirect(url_for('inscripcion.index'))