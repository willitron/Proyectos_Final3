from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Estudiante, Docente, Carrera, Materia, Inscripcion, Nota, Asignacion, Persona
from utils.decorators import permiso_requerido
from utils.pdf_generator import PDFGenerator
from datetime import datetime
import os

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reportes')

@reporte_bp.route('/')
@login_required
def index():
    """Página principal de reportes"""
    return render_template('reporte/index.html', current_year=datetime.now().year)

@reporte_bp.route('/estudiantes', methods=['GET', 'POST'])
@login_required
@permiso_requerido('ver_estudiantes')
def reporte_estudiantes():
    """Genera reporte de estudiantes"""
    if request.method == 'POST':
        # Obtener filtros
        carrera_id = request.form.get('carrera_id')
        activo = request.form.get('activo')
        
        # Consulta base
        query = Estudiante.query.join(Persona)
        
        # Aplicar filtros
        if carrera_id:
            query = query.join(Inscripcion).filter(Inscripcion.carrera_id == carrera_id)
        
        if activo:
            query = query.filter(Estudiante.activo == (activo == 'true'))
        
        estudiantes = query.all()
        
        # Generar PDF
        filename = f'reportes/estudiantes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        filepath = os.path.join('static', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        pdf = PDFGenerator(filepath, "REPORTE DE ESTUDIANTES")
        
        # Metadatos
        pdf.add_metadata(
            generated_by=current_user.username,
            user_role=current_user.roles[0].nombre if current_user.roles else "N/A",
            additional_info={
                "Total Registros": len(estudiantes),
                "Filtros Aplicados": "Carrera" if carrera_id else "Ninguno"
            }
        )
        
        # Título
        pdf.add_title()
        
        # Resumen
        pdf.add_summary_box({
            "Total de Estudiantes": len(estudiantes),
            "Activos": sum(1 for e in estudiantes if e.activo),
            "Inactivos": sum(1 for e in estudiantes if not e.activo)
        })
        
        # Tabla de datos
        if estudiantes:
            data = [['Código', 'Nombre Completo', 'CI', 'Carrera', 'Estado']]
            
            for est in estudiantes:
                inscripciones = Inscripcion.query.filter_by(estudiante_id=est.id).first()
                carrera_nombre = inscripciones.carrera.nombre if inscripciones else "Sin carrera"
                
                data.append([
                    est.codigo_estudiante or "N/A",
                    est.persona.nombre_completo,
                    est.persona.nro_documento,
                    carrera_nombre[:30],
                    "Activo" if est.activo else "Inactivo"
                ])
            
            pdf.add_section("Listado de Estudiantes")
            pdf.add_table(data, col_widths=[1.2*72, 2*72, 1*72, 2*72, 0.8*72])
        else:
            pdf.add_paragraph("No se encontraron estudiantes con los filtros aplicados.")
        
        # Firmas
        pdf.add_signature_section([
            "Secretaria General",
            "Director Académico"
        ])
        
        # Construir PDF
        pdf.build()
        
        return send_file(filepath, as_attachment=True, download_name=f'reporte_estudiantes_{datetime.now().strftime("%Y%m%d")}.pdf')
    
    # GET - Mostrar formulario
    carreras = Carrera.query.filter_by(activo=True).all()
    return render_template('reporte/estudiantes.html', carreras=carreras, now=datetime.now())

@reporte_bp.route('/notas/<int:inscripcion_id>')
@login_required
def reporte_notas_estudiante(inscripcion_id):
    """Genera reporte de notas de un estudiante"""
    inscripcion = Inscripcion.query.get_or_404(inscripcion_id)
    
    # Verificar permisos
    if not (current_user.tiene_permiso('ver_notas') or 
            (current_user.estudiante_id and current_user.estudiante_id == inscripcion.estudiante_id)):
        flash('No tienes permisos para ver este reporte.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Obtener notas
    notas = Nota.query.filter_by(inscripcion_id=inscripcion_id).join(Asignacion).all()
    
    # Generar PDF
    filename = f'reportes/notas_{inscripcion.estudiante.codigo_estudiante}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    filepath = os.path.join('static', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    pdf = PDFGenerator(filepath, "CERTIFICADO DE NOTAS")
    
    # Metadatos
    pdf.add_metadata(
        generated_by=current_user.username,
        user_role=current_user.roles[0].nombre if current_user.roles else "N/A",
        additional_info={
            "Estudiante": inscripcion.estudiante.persona.nombre_completo,
            "Carrera": inscripcion.carrera.nombre,
            "Gestión": inscripcion.gestion,
            "Periodo": inscripcion.periodo
        }
    )
    
    # Título
    pdf.add_title()
    
    # Información del estudiante
    pdf.add_section("Información del Estudiante")
    pdf.add_paragraph(f"""
        <b>Nombre:</b> {inscripcion.estudiante.persona.nombre_completo}<br/>
        <b>CI:</b> {inscripcion.estudiante.persona.nro_documento}<br/>
        <b>Código:</b> {inscripcion.estudiante.codigo_estudiante}<br/>
        <b>Carrera:</b> {inscripcion.carrera.nombre}<br/>
        <b>Gestión:</b> {inscripcion.gestion} - Periodo {inscripcion.periodo}
    """)
    
    pdf.add_spacer(0.3)
    
    # Tabla de notas
    if notas:
        data = [['Materia', '1er Parcial', '2do Parcial', '3er Parcial', 'Final', 'Estado']]
        
        total_promedio = 0
        materias_aprobadas = 0
        
        for nota in notas:
            materia_nombre = nota.asignacion.materia.nombre
            p1 = f"{nota.primer_parcial:.0f}" if nota.primer_parcial else "-"
            p2 = f"{nota.segundo_parcial:.0f}" if nota.segundo_parcial else "-"
            p3 = f"{nota.tercer_parcial:.0f}" if nota.tercer_parcial else "-"
            final = f"{nota.nota_final:.0f}" if nota.nota_final else "-"
            
            if nota.nota_final:
                estado = "Aprobado" if nota.nota_final >= 51 else "Reprobado"
                if nota.nota_final >= 51:
                    materias_aprobadas += 1
                total_promedio += nota.nota_final
            else:
                estado = "Pendiente"
            
            data.append([
                materia_nombre[:35],
                p1, p2, p3, final, estado
            ])
        
        pdf.add_section("Registro de Calificaciones")
        pdf.add_table(data, col_widths=[2.5*72, 0.8*72, 0.8*72, 0.8*72, 0.8*72, 1*72])
        
        # Resumen
        promedio_general = total_promedio / len(notas) if notas else 0
        pdf.add_summary_box({
            "Total Materias": len(notas),
            "Materias Aprobadas": materias_aprobadas,
            "Materias Reprobadas": len(notas) - materias_aprobadas,
            "Promedio General": f"{promedio_general:.2f}"
        })
    else:
        pdf.add_paragraph("No se registraron calificaciones para esta inscripción.")
    
    # Firmas
    pdf.add_signature_section([
        "Secretaria Académica",
        "Director de Carrera"
    ])
    
    # Construir PDF
    pdf.build()
    
    return send_file(filepath, as_attachment=True, download_name=f'certificado_notas_{inscripcion.estudiante.codigo_estudiante}.pdf')

@reporte_bp.route('/docentes')
@login_required
@permiso_requerido('ver_docentes')
def reporte_docentes():
    """Genera reporte de docentes con sus asignaciones"""
    docentes = Docente.query.filter_by(activo=True).join(Persona).all()
    
    # Generar PDF
    filename = f'reportes/docentes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    filepath = os.path.join('static', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    pdf = PDFGenerator(filepath, "REPORTE DE DOCENTES")
    
    # Metadatos
    pdf.add_metadata(
        generated_by=current_user.username,
        user_role=current_user.roles[0].nombre if current_user.roles else "N/A",
        additional_info={
            "Total Docentes": len(docentes)
        }
    )
    
    # Título
    pdf.add_title()
    
    # Resumen
    pdf.add_summary_box({
        "Total de Docentes Activos": len(docentes)
    })
    
    # Tabla de docentes
    data = [['Código', 'Nombre Completo', 'Grado', 'Materias Asignadas']]
    
    for doc in docentes:
        asignaciones = Asignacion.query.filter_by(docente_id=doc.id).count()
        
        data.append([
            doc.codigo_docente or "N/A",
            doc.persona.nombre_completo,
            doc.grado_academico or "N/A",
            str(asignaciones)
        ])
    
    pdf.add_section("Listado de Docentes")
    pdf.add_table(data, col_widths=[1*72, 2.5*72, 1.5*72, 1*72])
    
    # Firmas
    pdf.add_signature_section([
        "Director Académico",
        "Recursos Humanos"
    ])
    
    # Construir PDF
    pdf.build()
    
    return send_file(filepath, as_attachment=True, download_name=f'reporte_docentes_{datetime.now().strftime("%Y%m%d")}.pdf')

@reporte_bp.route('/carreras')
@login_required
@permiso_requerido('ver_carreras')
def reporte_carreras():
    """Genera reporte de carreras con estadísticas"""
    carreras = Carrera.query.filter_by(activo=True).all()
    
    # Generar PDF
    filename = f'reportes/carreras_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    filepath = os.path.join('static', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    pdf = PDFGenerator(filepath, "REPORTE DE CARRERAS")
    
    # Metadatos
    pdf.add_metadata(
        generated_by=current_user.username,
        user_role=current_user.roles[0].nombre if current_user.roles else "N/A"
    )
    
    # Título
    pdf.add_title()
    
    # Tabla de carreras
    data = [['Código', 'Nombre', 'Tipo', 'Estudiantes', 'Materias']]
    
    total_estudiantes = 0
    for carrera in carreras:
        estudiantes = Inscripcion.query.filter_by(carrera_id=carrera.id).distinct(Inscripcion.estudiante_id).count()
        materias = Materia.query.filter_by(carrera_id=carrera.id, activo=True).count()
        total_estudiantes += estudiantes
        
        data.append([
            carrera.codigo,
            carrera.nombre[:40],
            carrera.tipo,
            str(estudiantes),
            str(materias)
        ])
    
    pdf.add_section("Listado de Carreras")
    pdf.add_table(data, col_widths=[1*72, 2.5*72, 1*72, 1*72, 0.8*72])
    
    # Resumen
    pdf.add_summary_box({
        "Total Carreras Activas": len(carreras),
        "Total Estudiantes": total_estudiantes
    })
    
    # Firmas
    pdf.add_signature_section([
        "Director General",
        "Secretaria Académica"
    ])
    
    # Construir PDF
    pdf.build()
    
    return send_file(filepath, as_attachment=True, download_name=f'reporte_carreras_{datetime.now().strftime("%Y%m%d")}.pdf')

@reporte_bp.route('/inscripciones')
@login_required
@permiso_requerido('ver_inscripciones')
def reporte_inscripciones():
    """Genera reporte de inscripciones por gestión"""
    gestion = request.args.get('gestion', datetime.now().year)
    
    inscripciones = Inscripcion.query.filter_by(gestion=gestion).all()
    
    # Generar PDF
    filename = f'reportes/inscripciones_{gestion}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    filepath = os.path.join('static', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    pdf = PDFGenerator(filepath, f"REPORTE DE INSCRIPCIONES - GESTIÓN {gestion}")
    
    # Metadatos
    pdf.add_metadata(
        generated_by=current_user.username,
        user_role=current_user.roles[0].nombre if current_user.roles else "N/A",
        additional_info={
            "Gestión": gestion,
            "Total Inscripciones": len(inscripciones)
        }
    )
    
    # Título
    pdf.add_title()
    
    # Tabla de inscripciones
    data = [['Estudiante', 'Carrera', 'Periodo', 'Estado', 'Fecha']]
    
    for insc in inscripciones:
        data.append([
            insc.estudiante.persona.nombre_completo[:30],
            insc.carrera.nombre[:25],
            insc.periodo,
            insc.estado,
            insc.fecha_inscripcion.strftime("%d/%m/%Y")
        ])
    
    pdf.add_section(f"Inscripciones Gestión {gestion}")
    pdf.add_table(data, col_widths=[2*72, 1.8*72, 0.7*72, 1*72, 1*72])
    
    # Resumen por estado
    estados = {}
    for insc in inscripciones:
        estados[insc.estado] = estados.get(insc.estado, 0) + 1
    
    resumen = dict(estados)
    resumen["Total"] = len(inscripciones)
    pdf.add_summary_box(resumen)
    
    # Firmas
    pdf.add_signature_section([
        "Secretaria General"
    ])
    
    # Construir PDF
    pdf.build()
    
    return send_file(filepath, as_attachment=True, download_name=f'reporte_inscripciones_{gestion}.pdf')