from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Carrera, Estudiante, Docente, Materia, Inscripcion, Asignacion
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_carreras': Carrera.query.filter_by(activo=True).count(),
        'total_estudiantes': Estudiante.query.filter_by(activo=True).count(),
        'total_docentes': Docente.query.filter_by(activo=True).count(),
        'total_materias': Materia.query.filter_by(activo=True).count(),
        'total_inscripciones': Inscripcion.query.count(),
        'total_asignaciones': Asignacion.query.count()
    }
    
    carreras_recientes = Carrera.query.filter_by(activo=True).order_by(Carrera.created_at.desc()).limit(5).all()
    
    return render_template('main/dashboard.html', stats=stats, carreras=carreras_recientes, current_year=datetime.now().year)