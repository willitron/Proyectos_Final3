from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Materia, Carrera
from utils.decorators import permiso_requerido

materia_bp = Blueprint('materia', __name__, url_prefix='/materias')

@materia_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    materias = Materia.query.order_by(Materia.nombre).paginate(page=page, per_page=10, error_out=False)
    return render_template('materia/index.html', materias=materias)

@materia_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_materia')
def crear():
    if request.method == 'POST':
        try:
            materia = Materia(
                codigo=request.form['codigo'],
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion'),
                carga_horaria=int(request.form.get('carga_horaria', 0)),
                horas_teoricas=int(request.form.get('horas_teoricas', 0)),
                horas_practicas=int(request.form.get('horas_practicas', 0)),
                creditos=int(request.form.get('creditos', 0)),
                semestre=int(request.form.get('semestre')) if request.form.get('semestre') else None,
                carrera_id=int(request.form.get('carrera_id')) if request.form.get('carrera_id') else None,
                requerido_para_semestre=bool(request.form.get('requerido_para_semestre')),
                activo=bool(request.form.get('activo'))
            )
            db.session.add(materia)
            db.session.commit()
            flash('Materia creada exitosamente.', 'success')
            return redirect(url_for('materia.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear materia: {str(e)}', 'danger')
    
    carreras = Carrera.query.filter_by(activo=True).all()
    return render_template('materia/crear.html', carreras=carreras)

@materia_bp.route('/<int:id>')
@login_required
def detalle(id):
    materia = Materia.query.get_or_404(id)
    return render_template('materia/detalle.html', materia=materia)

@materia_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_materia')
def editar(id):
    materia = Materia.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            materia.codigo = request.form['codigo']
            materia.nombre = request.form['nombre']
            materia.descripcion = request.form.get('descripcion')
            materia.carga_horaria = int(request.form.get('carga_horaria', 0))
            materia.horas_teoricas = int(request.form.get('horas_teoricas', 0))
            materia.horas_practicas = int(request.form.get('horas_practicas', 0))
            materia.creditos = int(request.form.get('creditos', 0))
            materia.semestre = int(request.form.get('semestre')) if request.form.get('semestre') else None
            materia.carrera_id = int(request.form.get('carrera_id')) if request.form.get('carrera_id') else None
            materia.requerido_para_semestre = bool(request.form.get('requerido_para_semestre'))
            materia.activo = bool(request.form.get('activo'))
            
            db.session.commit()
            flash('Materia actualizada exitosamente.', 'success')
            return redirect(url_for('materia.detalle', id=materia.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar materia: {str(e)}', 'danger')
    
    carreras = Carrera.query.filter_by(activo=True).all()
    return render_template('materia/editar.html', materia=materia, carreras=carreras)

@materia_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_materia')
def eliminar(id):
    materia = Materia.query.get_or_404(id)
    
    try:
        db.session.delete(materia)
        db.session.commit()
        flash('Materia eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar materia: {str(e)}', 'danger')
    
    return redirect(url_for('materia.index'))