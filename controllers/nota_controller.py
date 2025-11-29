from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Nota, Inscripcion, Asignacion
from utils.decorators import permiso_requerido

nota_bp = Blueprint('nota', __name__, url_prefix='/notas')

@nota_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    notas = Nota.query.order_by(Nota.fecha_registro.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('nota/index.html', notas=notas)

@nota_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@permiso_requerido('crear_nota')
def crear():
    if request.method == 'POST':
        try:
            primer_parcial = float(request.form.get('primer_parcial')) if request.form.get('primer_parcial') else None
            segundo_parcial = float(request.form.get('segundo_parcial')) if request.form.get('segundo_parcial') else None
            tercer_parcial = float(request.form.get('tercer_parcial')) if request.form.get('tercer_parcial') else None
            
            # primedio
            notas_validas = [n for n in [primer_parcial, segundo_parcial, tercer_parcial] if n is not None]
            promedio = sum(notas_validas) / len(notas_validas) if notas_validas else None
            
            nota = Nota(
                inscripcion_id=int(request.form['inscripcion_id']),
                asignacion_id=int(request.form['asignacion_id']),
                primer_parcial=primer_parcial,
                segundo_parcial=segundo_parcial,
                tercer_parcial=tercer_parcial,
                nota_final=float(request.form.get('nota_final')) if request.form.get('nota_final') else promedio,
                promedio=promedio,
                observaciones=request.form.get('observaciones'),
                estado=request.form.get('estado', 'Abierto')
            )
            db.session.add(nota)
            db.session.commit()
            flash('Nota creada exitosamente.', 'success')
            return redirect(url_for('nota.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear nota: {str(e)}', 'danger')
    
    inscripciones = Inscripcion.query.all()
    asignaciones = Asignacion.query.all()
    return render_template('nota/crear.html', inscripciones=inscripciones, asignaciones=asignaciones)

@nota_bp.route('/<int:id>')
@login_required
def detalle(id):
    nota = Nota.query.get_or_404(id)
    return render_template('nota/detalle.html', nota=nota)

@nota_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_nota')
def editar(id):
    nota = Nota.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            primer_parcial = float(request.form.get('primer_parcial')) if request.form.get('primer_parcial') else None
            segundo_parcial = float(request.form.get('segundo_parcial')) if request.form.get('segundo_parcial') else None
            tercer_parcial = float(request.form.get('tercer_parcial')) if request.form.get('tercer_parcial') else None
            
            notas_validas = [n for n in [primer_parcial, segundo_parcial, tercer_parcial] if n is not None]
            promedio = sum(notas_validas) / len(notas_validas) if notas_validas else None
            
            nota.inscripcion_id = int(request.form['inscripcion_id'])
            nota.asignacion_id = int(request.form['asignacion_id'])
            nota.primer_parcial = primer_parcial
            nota.segundo_parcial = segundo_parcial
            nota.tercer_parcial = tercer_parcial
            nota.nota_final = float(request.form.get('nota_final')) if request.form.get('nota_final') else promedio
            nota.promedio = promedio
            nota.observaciones = request.form.get('observaciones')
            nota.estado = request.form.get('estado', 'Abierto')
            
            db.session.commit()
            flash('Nota actualizada exitosamente.', 'success')
            return redirect(url_for('nota.detalle', id=nota.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar nota: {str(e)}', 'danger')
    
    inscripciones = Inscripcion.query.all()
    asignaciones = Asignacion.query.all()
    return render_template('nota/editar.html', nota=nota, inscripciones=inscripciones, asignaciones=asignaciones)

@nota_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@permiso_requerido('eliminar_nota')
def eliminar(id):
    nota = Nota.query.get_or_404(id)
    
    try:
        db.session.delete(nota)
        db.session.commit()
        flash('Nota eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar nota: {str(e)}', 'danger')
    
    return redirect(url_for('nota.index'))