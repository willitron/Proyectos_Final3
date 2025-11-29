from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Estudiante, Persona
from utils.decorators import permiso_requerido

estudiante_bp = Blueprint('estudiante', __name__, url_prefix='/estudiantes')

@estudiante_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    estudiantes = Estudiante.query.join(Persona).order_by(Persona.apellido_paterno).paginate(page=page, per_page=10, error_out=False)
    return render_template('estudiante/index.html', estudiantes=estudiantes)

@estudiante_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_estudiante')
def crear():
    if request.method == 'POST':
        try:
            estudiante = Estudiante(
                persona_id=int(request.form['persona_id']),
                codigo_estudiante=request.form['codigo_estudiante'],
                nacionalidad=request.form.get('nacionalidad'),
                provincia=request.form.get('provincia'),
                departamento=request.form.get('departamento'),
                estado_civil=request.form.get('estado_civil', 'Soltero'),
                idioma_orig=request.form.get('idioma_orig'),
                comunidad=request.form.get('comunidad'),
                zona=request.form.get('zona'),
                colegio_egreso=request.form.get('colegio_egreso'),
                anio_egreso=int(request.form.get('anio_egreso')) if request.form.get('anio_egreso') else None,
                tipo_ingreso=request.form.get('tipo_ingreso', 'Regular'),
                activo=bool(request.form.get('activo'))
            )
            db.session.add(estudiante)
            db.session.commit()
            flash('Estudiante creado exitosamente.', 'success')
            return redirect(url_for('estudiante.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear estudiante: {str(e)}', 'danger')
    
    personas = Persona.query.outerjoin(Estudiante).filter(Estudiante.id == None).all()
    return render_template('estudiante/crear.html', personas=personas)

@estudiante_bp.route('/<int:id>')
@login_required
def detalle(id):
    estudiante = Estudiante.query.get_or_404(id)
    return render_template('estudiante/detalle.html', estudiante=estudiante)

@estudiante_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_estudiante')
def editar(id):
    estudiante = Estudiante.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            estudiante.codigo_estudiante = request.form['codigo_estudiante']
            estudiante.nacionalidad = request.form.get('nacionalidad')
            estudiante.provincia = request.form.get('provincia')
            estudiante.departamento = request.form.get('departamento')
            estudiante.estado_civil = request.form.get('estado_civil', 'Soltero')
            estudiante.idioma_orig = request.form.get('idioma_orig')
            estudiante.comunidad = request.form.get('comunidad')
            estudiante.zona = request.form.get('zona')
            estudiante.colegio_egreso = request.form.get('colegio_egreso')
            estudiante.anio_egreso = int(request.form.get('anio_egreso')) if request.form.get('anio_egreso') else None
            estudiante.tipo_ingreso = request.form.get('tipo_ingreso', 'Regular')
            estudiante.activo = bool(request.form.get('activo'))
            
            db.session.commit()
            flash('Estudiante actualizado exitosamente.', 'success')
            return redirect(url_for('estudiante.detalle', id=estudiante.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar estudiante: {str(e)}', 'danger')
    
    return render_template('estudiante/editar.html', estudiante=estudiante)

@estudiante_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_estudiante')
def eliminar(id):
    estudiante = Estudiante.query.get_or_404(id)
    
    try:
        db.session.delete(estudiante)
        db.session.commit()
        flash('Estudiante eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar estudiante: {str(e)}', 'danger')
    
    return redirect(url_for('estudiante.index'))