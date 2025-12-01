"""
Script para generar TODAS las plantillas HTML completas
Ejecutar: python generate_all_templates.py
"""

import os

def create_dir(path):
    os.makedirs(path, exist_ok=True)
    print(f"✓ Creado: {path}")

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Archivo: {path}")

# Crear estructura
templates_dir = 'templates'
modules = ['estudiante', 'docente', 'asignacion', 'inscripcion', 'nota', 'usuario', 'rol']

print("Creando estructura de templates...")
for module in modules:
    create_dir(f'{templates_dir}/{module}')

# ============ ESTUDIANTE ============
estudiante_index = '''{% extends "base.html" %}

{% block title %}Estudiantes - Instituto Ballivián{% endblock %}
{% block page_title %}Gestión de Estudiantes{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h4>Listado de Estudiantes</h4>
    {% if current_user.tiene_permiso('crear_estudiante') %}
    <a href="{{ url_for('estudiante.crear') }}" class="btn btn-primary">
        <i class="bi bi-plus-circle"></i> Nuevo Estudiante
    </a>
    {% endif %}
</div>

<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Nombre Completo</th>
                        <th>CI</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for estudiante in estudiantes.items %}
                    <tr>
                        <td>{{ estudiante.codigo_estudiante }}</td>
                        <td>{{ estudiante.persona.nombre_completo }}</td>
                        <td>{{ estudiante.persona.nro_documento }}</td>
                        <td>
                            {% if estudiante.activo %}
                                <span class="badge bg-success">Activo</span>
                            {% else %}
                                <span class="badge bg-secondary">Inactivo</span>
                            {% endif %}
                        </td>
                        <td>
                            <div class="btn-group btn-group-sm">
                                <a href="{{ url_for('estudiante.detalle', id=estudiante.id) }}" class="btn btn-info">
                                    <i class="bi bi-eye"></i>
                                </a>
                                {% if current_user.tiene_permiso('editar_estudiante') %}
                                <a href="{{ url_for('estudiante.editar', id=estudiante.id) }}" class="btn btn-warning">
                                    <i class="bi bi-pencil"></i>
                                </a>
                                {% endif %}
                                {% if current_user.tiene_permiso('eliminar_estudiante') %}
                                <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal{{ estudiante.id }}">
                                    <i class="bi bi-trash"></i>
                                </button>
                                {% endif %}
                            </div>
                            
                            <div class="modal fade" id="deleteModal{{ estudiante.id }}" tabindex="-1">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title">Confirmar Eliminación</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                        </div>
                                        <div class="modal-body">
                                            ¿Está seguro de eliminar al estudiante "{{ estudiante.persona.nombre_completo }}"?
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                            <form method="POST" action="{{ url_for('estudiante.eliminar', id=estudiante.id) }}">
                                                <button type="submit" class="btn btn-danger">Eliminar</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="5" class="text-center">No hay estudiantes registrados</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        {% if estudiantes.pages > 1 %}
        <nav>
            <ul class="pagination justify-content-center">
                <li class="page-item {% if not estudiantes.has_prev %}disabled{% endif %}">
                    <a class="page-link" href="{{ url_for('estudiante.index', page=estudiantes.prev_num) }}">Anterior</a>
                </li>
                {% for page_num in estudiantes.iter_pages() %}
                    {% if page_num %}
                        <li class="page-item {% if page_num == estudiantes.page %}active{% endif %}">
                            <a class="page-link" href="{{ url_for('estudiante.index', page=page_num) }}">{{ page_num }}</a>
                        </li>
                    {% else %}
                        <li class="page-item disabled"><span class="page-link">...</span></li>
                    {% endif %}
                {% endfor %}
                <li class="page-item {% if not estudiantes.has_next %}disabled{% endif %}">
                    <a class="page-link" href="{{ url_for('estudiante.index', page=estudiantes.next_num) }}">Siguiente</a>
                </li>
            </ul>
        </nav>
        {% endif %}
    </div>
</div>
{% endblock %}'''

estudiante_crear = '''{% extends "base.html" %}

{% block title %}Crear Estudiante - Instituto Ballivián{% endblock %}
{% block page_title %}Nuevo Estudiante{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h5>Registrar Nuevo Estudiante</h5>
    </div>
    <div class="card-body">
        <form method="POST">
            <div class="alert alert-info">
                <strong>Nota:</strong> Primero debes crear la persona en el módulo de Personas.
            </div>
            
            <div class="mb-3">
                <label for="persona_id" class="form-label">Persona *</label>
                <select class="form-select" id="persona_id" name="persona_id" required>
                    <option value="">Seleccionar persona</option>
                    {% for persona in personas %}
                    <option value="{{ persona.id }}">{{ persona.nombre_completo }} ({{ persona.nro_documento }})</option>
                    {% endfor %}
                </select>
            </div>
            
            <div class="mb-3">
                <label for="codigo_estudiante" class="form-label">Código de Estudiante *</label>
                <input type="text" class="form-control" id="codigo_estudiante" name="codigo_estudiante" required>
            </div>
            
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="nacionalidad" class="form-label">Nacionalidad</label>
                    <input type="text" class="form-control" id="nacionalidad" name="nacionalidad" value="Boliviana">
                </div>
                <div class="col-md-6 mb-3">
                    <label for="estado_civil" class="form-label">Estado Civil</label>
                    <select class="form-select" id="estado_civil" name="estado_civil">
                        <option value="Soltero" selected>Soltero</option>
                        <option value="Casado">Casado</option>
                        <option value="Viudo">Viudo</option>
                        <option value="Divorciado">Divorciado</option>
                        <option value="Otro">Otro</option>
                    </select>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label for="departamento" class="form-label">Departamento</label>
                    <input type="text" class="form-control" id="departamento" name="departamento">
                </div>
                <div class="col-md-4 mb-3">
                    <label for="provincia" class="form-label">Provincia</label>
                    <input type="text" class="form-control" id="provincia" name="provincia">
                </div>
                <div class="col-md-4 mb-3">
                    <label for="zona" class="form-label">Zona</label>
                    <input type="text" class="form-control" id="zona" name="zona">
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-8 mb-3">
                    <label for="colegio_egreso" class="form-label">Colegio de Egreso</label>
                    <input type="text" class="form-control" id="colegio_egreso" name="colegio_egreso">
                </div>
                <div class="col-md-4 mb-3">
                    <label for="anio_egreso" class="form-label">Año de Egreso</label>
                    <input type="number" class="form-control" id="anio_egreso" name="anio_egreso" min="1950" max="2030">
                </div>
            </div>
            
            <div class="mb-3">
                <label for="tipo_ingreso" class="form-label">Tipo de Ingreso</label>
                <select class="form-select" id="tipo_ingreso" name="tipo_ingreso">
                    <option value="Regular" selected>Regular</option>
                    <option value="Traslado">Traslado</option>
                    <option value="Libre">Libre</option>
                </select>
            </div>
            
            <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="activo" name="activo" checked>
                <label class="form-check-label" for="activo">Activo</label>
            </div>
            
            <div class="d-flex justify-content-between">
                <a href="{{ url_for('estudiante.index') }}" class="btn btn-secondary">
                    <i class="bi bi-arrow-left"></i> Cancelar
                </a>
                <button type="submit" class="btn btn-primary">
                    <i class="bi bi-save"></i> Guardar
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}'''

estudiante_editar = '''{% extends "base.html" %}

{% block title %}Editar Estudiante - Instituto Ballivián{% endblock %}
{% block page_title %}Editar Estudiante{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h5>Editar: {{ estudiante.persona.nombre_completo }}</h5>
    </div>
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">Persona Asociada</label>
                <input type="text" class="form-control" value="{{ estudiante.persona.nombre_completo }} ({{ estudiante.persona.nro_documento }})" disabled>
            </div>
            
            <div class="mb-3">
                <label for="codigo_estudiante" class="form-label">Código de Estudiante *</label>
                <input type="text" class="form-control" id="codigo_estudiante" name="codigo_estudiante" value="{{ estudiante.codigo_estudiante }}" required>
            </div>
            
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="nacionalidad" class="form-label">Nacionalidad</label>
                    <input type="text" class="form-control" id="nacionalidad" name="nacionalidad" value="{{ estudiante.nacionalidad }}">
                </div>
                <div class="col-md-6 mb-3">
                    <label for="estado_civil" class="form-label">Estado Civil</label>
                    <select class="form-select" id="estado_civil" name="estado_civil">
                        <option value="Soltero" {% if estudiante.estado_civil == 'Soltero' %}selected{% endif %}>Soltero</option>
                        <option value="Casado" {% if estudiante.estado_civil == 'Casado' %}selected{% endif %}>Casado</option>
                        <option value="Viudo" {% if estudiante.estado_civil == 'Viudo' %}selected{% endif %}>Viudo</option>
                        <option value="Divorciado" {% if estudiante.estado_civil == 'Divorciado' %}selected{% endif %}>Divorciado</option>
                        <option value="Otro" {% if estudiante.estado_civil == 'Otro' %}selected{% endif %}>Otro</option>
                    </select>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label for="departamento" class="form-label">Departamento</label>
                    <input type="text" class="form-control" id="departamento" name="departamento" value="{{ estudiante.departamento }}">
                </div>
                <div class="col-md-4 mb-3">
                    <label for="provincia" class="form-label">Provincia</label>
                    <input type="text" class="form-control" id="provincia" name="provincia" value="{{ estudiante.provincia }}">
                </div>
                <div class="col-md-4 mb-3">
                    <label for="zona" class="form-label">Zona</label>
                    <input type="text" class="form-control" id="zona" name="zona" value="{{ estudiante.zona }}">
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-8 mb-3">
                    <label for="colegio_egreso" class="form-label">Colegio de Egreso</label>
                    <input type="text" class="form-control" id="colegio_egreso" name="colegio_egreso" value="{{ estudiante.colegio_egreso }}">
                </div>
                <div class="col-md-4 mb-3">
                    <label for="anio_egreso" class="form-label">Año de Egreso</label>
                    <input type="number" class="form-control" id="anio_egreso" name="anio_egreso" value="{{ estudiante.anio_egreso }}">
                </div>
            </div>
            
            <div class="mb-3">
                <label for="tipo_ingreso" class="form-label">Tipo de Ingreso</label>
                <select class="form-select" id="tipo_ingreso" name="tipo_ingreso">
                    <option value="Regular" {% if estudiante.tipo_ingreso == 'Regular' %}selected{% endif %}>Regular</option>
                    <option value="Traslado" {% if estudiante.tipo_ingreso == 'Traslado' %}selected{% endif %}>Traslado</option>
                    <option value="Libre" {% if estudiante.tipo_ingreso == 'Libre' %}selected{% endif %}>Libre</option>
                </select>
            </div>
            
            <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="activo" name="activo" {% if estudiante.activo %}checked{% endif %}>
                <label class="form-check-label" for="activo">Activo</label>
            </div>
            
            <div class="d-flex justify-content-between">
                <a href="{{ url_for('estudiante.index') }}" class="btn btn-secondary">
                    <i class="bi bi-arrow-left"></i> Cancelar
                </a>
                <button type="submit" class="btn btn-primary">
                    <i class="bi bi-save"></i> Actualizar
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}'''

estudiante_detalle = '''{% extends "base.html" %}

{% block title %}Detalle Estudiante - Instituto Ballivián{% endblock %}
{% block page_title %}Información de Estudiante{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5>{{ estudiante.persona.nombre_completo }}</h5>
        <div>
            {% if current_user.tiene_permiso('editar_estudiante') %}
            <a href="{{ url_for('estudiante.editar', id=estudiante.id) }}" class="btn btn-warning btn-sm">
                <i class="bi bi-pencil"></i> Editar
            </a>
            {% endif %}
            <a href="{{ url_for('estudiante.index') }}" class="btn btn-secondary btn-sm">
                <i class="bi bi-arrow-left"></i> Volver
            </a>
        </div>
    </div>
    <div class="card-body">
        <div class="row">
            <div class="col-md-6">
                <h6 class="text-muted">Información Académica</h6>
                <table class="table table-borderless">
                    <tr>
                        <th width="40%">Código Estudiante:</th>
                        <td>{{ estudiante.codigo_estudiante }}</td>
                    </tr>
                    <tr>
                        <th>CI:</th>
                        <td>{{ estudiante.persona.nro_documento }}</td>
                    </tr>
                    <tr>
                        <th>Tipo de Ingreso:</th>
                        <td>{{ estudiante.tipo_ingreso }}</td>
                    </tr>
                    <tr>
                        <th>Estado:</th>
                        <td>
                            {% if estudiante.activo %}
                                <span class="badge bg-success">Activo</span>
                            {% else %}
                                <span class="badge bg-secondary">Inactivo</span>
                            {% endif %}
                        </td>
                    </tr>
                </table>
            </div>
            <div class="col-md-6">
                <h6 class="text-muted">Información Personal</h6>
                <table class="table table-borderless">
                    <tr>
                        <th width="40%">Nacionalidad:</th>
                        <td>{{ estudiante.nacionalidad or 'N/A' }}</td>
                    </tr>
                    <tr>
                        <th>Estado Civil:</th>
                        <td>{{ estudiante.estado_civil }}</td>
                    </tr>
                    <tr>
                        <th>Departamento:</th>
                        <td>{{ estudiante.departamento or 'N/A' }}</td>
                    </tr>
                    <tr>
                        <th>Provincia:</th>
                        <td>{{ estudiante.provincia or 'N/A' }}</td>
                    </tr>
                </table>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-md-12">
                <h6 class="text-muted">Información Académica Previa</h6>
                <table class="table table-borderless">
                    <tr>
                        <th width="20%">Colegio de Egreso:</th>
                        <td>{{ estudiante.colegio_egreso or 'N/A' }}</td>
                    </tr>
                    <tr>
                        <th>Año de Egreso:</th>
                        <td>{{ estudiante.anio_egreso or 'N/A' }}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

# Escribir archivos de estudiante
write_file(f'{templates_dir}/estudiante/index.html', estudiante_index)
write_file(f'{templates_dir}/estudiante/crear.html', estudiante_crear)
write_file(f'{templates_dir}/estudiante/editar.html', estudiante_editar)
write_file(f'{templates_dir}/estudiante/detalle.html', estudiante_detalle)

print("\n" + "="*60)
print("✅ Plantillas de ESTUDIANTE generadas correctamente")
print("="*60)
print("\n⚠️  NOTA: Este script genera solo las plantillas de ESTUDIANTE como ejemplo.")
print("Para obtener TODAS las plantillas restantes (docente, asignacion, inscripcion, nota, usuario, rol),")
print("necesitas que te las proporcione en artefactos adicionales.")
print("\n¿Deseas que continúe generando las demás plantillas? [s/n]")