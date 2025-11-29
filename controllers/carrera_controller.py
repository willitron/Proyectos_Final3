from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Carrera
from utils.decorators import permiso_requerido
from datetime import datetime

carrera_bp = Blueprint('carrera', __name__, url_prefix='/carreras')

@carrera_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    carreras = Carrera.query.order_by(Carrera.nombre).paginate(page=page, per_page=10, error_out=False)
    return render_template('carrera/index.html', carreras=carreras)

@carrera_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_carrera')
def crear():
    if request.method == 'POST':
        try:
            carrera = Carrera(
                codigo=request.form['codigo'],
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion'),
                tipo=request.form['tipo'],
                carga_horaria=int(request.form.get('carga_horaria', 0)),
                creditos=int(request.form.get('creditos', 0)) if request.form.get('creditos') else None,
                fecha_creacion=datetime.strptime(request.form['fecha_creacion'], '%Y-%m-%d').date() if request.form.get('fecha_creacion') else None,
                activo=bool(request.form.get('activo'))
            )
            db.session.add(carrera)
            db.session.commit()
            flash('Carrera creada exitosamente.', 'success')
            return redirect(url_for('carrera.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear carrera: {str(e)}', 'danger')
    
    return render_template('carrera/crear.html')

@carrera_bp.route('/<int:id>')
@login_required
def detalle(id):
    carrera = Carrera.query.get_or_404(id)
    return render_template('carrera/detalle.html', carrera=carrera)

@carrera_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_carrera')
def editar(id):
    carrera = Carrera.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            carrera.codigo = request.form['codigo']
            carrera.nombre = request.form['nombre']
            carrera.descripcion = request.form.get('descripcion')
            carrera.tipo = request.form['tipo']
            carrera.carga_horaria = int(request.form.get('carga_horaria', 0))
            carrera.creditos = int(request.form.get('creditos', 0)) if request.form.get('creditos') else None
            carrera.fecha_creacion = datetime.strptime(request.form['fecha_creacion'], '%Y-%m-%d').date() if request.form.get('fecha_creacion') else None
            carrera.activo = bool(request.form.get('activo'))
            
            db.session.commit()
            flash('Carrera actualizada exitosamente.', 'success')
            return redirect(url_for('carrera.detalle', id=carrera.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar carrera: {str(e)}', 'danger')
    
    return render_template('carrera/editar.html', carrera=carrera)

@carrera_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_carrera')
def eliminar(id):
    carrera = Carrera.query.get_or_404(id)
    
    try:
        db.session.delete(carrera)
        db.session.commit()
        flash('Carrera eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar carrera: {str(e)}', 'danger')
    
    return redirect(url_for('carrera.index'))