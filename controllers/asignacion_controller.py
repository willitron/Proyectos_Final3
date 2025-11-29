from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Asignacion, Materia, Docente, Carrera
from utils.decorators import permiso_requerido

asignacion_bp = Blueprint('asignacion', __name__, url_prefix='/asignaciones')

@asignacion_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    asignaciones = Asignacion.query.order_by(Asignacion.gestion.desc(), Asignacion.periodo).paginate(page=page, per_page=10, error_out=False)
    return render_template('asignacion/index.html', asignaciones=asignaciones)

@asignacion_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_asignacion')
def crear():
    if request.method == 'POST':
        try:
            asignacion = Asignacion(
                materia_id=int(request.form['materia_id']),
                docente_id=int(request.form['docente_id']),
                carrera_id=int(request.form['carrera_id']) if request.form.get('carrera_id') else None,
                gestion=int(request.form['gestion']),
                periodo=request.form['periodo'],
                codigo_grupo=request.form.get('codigo_grupo'),
                horario=request.form.get('horario'),
                tipo_imparticion=request.form.get('tipo_imparticion', 'Presencial'),
                cupo=int(request.form.get('cupo')) if request.form.get('cupo') else None
            )
            db.session.add(asignacion)
            db.session.commit()
            flash('Asignación creada exitosamente.', 'success')
            return redirect(url_for('asignacion.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear asignación: {str(e)}', 'danger')
    
    materias = Materia.query.filter_by(activo=True).all()
    docentes = Docente.query.filter_by(activo=True).all()
    carreras = Carrera.query.filter_by(activo=True).all()
    return render_template('asignacion/crear.html', materias=materias, docentes=docentes, carreras=carreras)

@asignacion_bp.route('/<int:id>')
@login_required
def detalle(id):
    asignacion = Asignacion.query.get_or_404(id)
    return render_template('asignacion/detalle.html', asignacion=asignacion)

@asignacion_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_asignacion')
def editar(id):
    asignacion = Asignacion.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            asignacion.materia_id = int(request.form['materia_id'])
            asignacion.docente_id = int(request.form['docente_id'])
            asignacion.carrera_id = int(request.form['carrera_id']) if request.form.get('carrera_id') else None
            asignacion.gestion = int(request.form['gestion'])
            asignacion.periodo = request.form['periodo']
            asignacion.codigo_grupo = request.form.get('codigo_grupo')
            asignacion.horario = request.form.get('horario')
            asignacion.tipo_imparticion = request.form.get('tipo_imparticion', 'Presencial')
            asignacion.cupo = int(request.form.get('cupo')) if request.form.get('cupo') else None
            
            db.session.commit()
            flash('Asignación actualizada exitosamente.', 'success')
            return redirect(url_for('asignacion.detalle', id=asignacion.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar asignación: {str(e)}', 'danger')
    
    materias = Materia.query.filter_by(activo=True).all()
    docentes = Docente.query.filter_by(activo=True).all()
    carreras = Carrera.query.filter_by(activo=True).all()
    return render_template('asignacion/editar.html', asignacion=asignacion, materias=materias, docentes=docentes, carreras=carreras)

@asignacion_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_asignacion')
def eliminar(id):
    asignacion = Asignacion.query.get_or_404(id)
    
    try:
        db.session.delete(asignacion)
        db.session.commit()
        flash('Asignación eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar asignación: {str(e)}', 'danger')
    
    return redirect(url_for('asignacion.index'))