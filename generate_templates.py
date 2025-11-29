

import os

TEMPLATES = {
    'materia': {
        'campos': ['codigo', 'nombre', 'descripcion', 'carga_horaria', 'horas_teoricas', 'horas_practicas', 'creditos', 'semestre', 'carrera_id', 'activo'],
        'relaciones': [('carrera_id', 'carrera', 'carreras')]
    },
    'persona': {
        'campos': ['tipo_documento', 'nro_documento', 'nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'sexo', 'lugar_nacimiento', 'direccion', 'telefono', 'email'],
        'relaciones': []
    },
    'estudiante': {
        'campos': ['persona_id', 'codigo_estudiante', 'nacionalidad', 'provincia', 'departamento', 'estado_civil', 'colegio_egreso', 'anio_egreso', 'tipo_ingreso', 'activo'],
        'relaciones': [('persona_id', 'persona', 'personas')]
    },
    'docente': {
        'campos': ['persona_id', 'codigo_docente', 'grado_academico', 'fecha_ingreso', 'fecha_nacimiento', 'titulo_universitario', 'activo'],
        'relaciones': [('persona_id', 'persona', 'personas')]
    },
    'asignacion': {
        'campos': ['materia_id', 'docente_id', 'carrera_id', 'gestion', 'periodo', 'codigo_grupo', 'horario', 'tipo_imparticion', 'cupo'],
        'relaciones': [('materia_id', 'materia', 'materias'), ('docente_id', 'docente', 'docentes'), ('carrera_id', 'carrera', 'carreras')]
    },
    'inscripcion': {
        'campos': ['estudiante_id', 'carrera_id', 'gestion', 'periodo', 'estado', 'metodo_ingreso'],
        'relaciones': [('estudiante_id', 'estudiante', 'estudiantes'), ('carrera_id', 'carrera', 'carreras')]
    },
    'nota': {
        'campos': ['inscripcion_id', 'asignacion_id', 'primer_parcial', 'segundo_parcial', 'tercer_parcial', 'nota_final', 'observaciones', 'estado'],
        'relaciones': [('inscripcion_id', 'inscripcion', 'inscripciones'), ('asignacion_id', 'asignacion', 'asignaciones')]
    },
    'usuario': {
        'campos': ['username', 'email', 'password', 'persona_id', 'estudiante_id', 'docente_id', 'activo', 'roles'],
        'relaciones': [('persona_id', 'persona', 'personas'), ('estudiante_id', 'estudiante', 'estudiantes'), ('docente_id', 'docente', 'docentes')]
    },
    'rol': {
        'campos': ['nombre', 'descripcion', 'permisos'],
        'relaciones': []
    }
}

def create_directory_structure():
    base_dir = 'templates'
    dirs = [
        'auth', 'main', 'errors',
        'carrera', 'materia', 'persona', 'estudiante', 'docente',
        'asignacion', 'inscripcion', 'nota', 'usuario', 'rol'
    ]
    
    for d in dirs:
        path = os.path.join(base_dir, d)
        os.makedirs(path, exist_ok=True)
        print(f"Creado directorio: {path}")

def generate_index_template(module_name, title):
    """Genera template index.html genérico"""
    return f'''{{%extends "base.html" %}}

{{%block title %}}{title} - Instituto Ballivián{{%endblock %}}
{{%block page_title %}}Gestión de {title}{{%endblock %}}

{{%block content %}}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h4>Listado de {title}</h4>
    {{%if current_user.tiene_permiso('crear_{module_name}') %}}
    <a href="{{{{url_for('{module_name}.crear') }}}}" class="btn btn-primary">
        <i class="bi bi-plus-circle"></i> Nuevo/a
    </a>
    {{%endif %}}
</div>

<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Información</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {{%for item in items.items %}}
                    <tr>
                        <td>{{{{item.id}}}}</td>
                        <td>{{{{item}}}}</td>
                        <td><span class="badge bg-success">Activo</span></td>
                        <td>
                            <div class="btn-group btn-group-sm">
                                <a href="{{{{url_for('{module_name}.detalle', id=item.id) }}}}" class="btn btn-info">
                                    <i class="bi bi-eye"></i>
                                </a>
                                {{%if current_user.tiene_permiso('editar_{module_name}') %}}
                                <a href="{{{{url_for('{module_name}.editar', id=item.id) }}}}" class="btn btn-warning">
                                    <i class="bi bi-pencil"></i>
                                </a>
                                {{%endif %}}
                                {{%if current_user.tiene_permiso('eliminar_{module_name}') %}}
                                <form method="POST" action="{{{{url_for('{module_name}.eliminar', id=item.id) }}}}" style="display:inline;" onsubmit="return confirm('¿Está seguro?');">
                                    <button type="submit" class="btn btn-danger">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </form>
                                {{%endif %}}
                            </div>
                        </td>
                    </tr>
                    {{%else %}}
                    <tr>
                        <td colspan="4" class="text-center">No hay registros</td>
                    </tr>
                    {{%endfor %}}
                </tbody>
            </table>
        </div>
    </div>
</div>
{{%endblock %}}'''

def generate_crear_template(module_name, title, campos):
    form_fields = ''
    for campo in campos[:5]:  
        form_fields += f'''
            <div class="mb-3">
                <label for="{campo}" class="form-label">{campo.replace('_', ' ').title()}</label>
                <input type="text" class="form-control" id="{campo}" name="{campo}">
            </div>'''
    
    return f'''{{%extends "base.html" %}}

{{%block title %}}Crear {title} - Instituto Ballivián{{%endblock %}}
{{%block page_title %}}Nuevo/a {title}{{%endblock %}}

{{%block content %}}
<div class="card">
    <div class="card-header">
        <h5>Crear Nuevo/a {title}</h5>
    </div>
    <div class="card-body">
        <form method="POST">
            {form_fields}
            
            <div class="d-flex justify-content-between">
                <a href="{{{{url_for('{module_name}.index') }}}}" class="btn btn-secondary">
                    <i class="bi bi-arrow-left"></i> Cancelar
                </a>
                <button type="submit" class="btn btn-primary">
                    <i class="bi bi-save"></i> Guardar
                </button>
            </div>
        </form>
    </div>
</div>
{{%endblock %}}'''

def generate_editar_template(module_name, title):
    return f'''{{%extends "base.html" %}}

{{%block title %}}Editar {title} - Instituto Ballivián{{%endblock %}}
{{%block page_title %}}Editar {title}{{%endblock %}}

{{%block content %}}
<div class="card">
    <div class="card-header">
        <h5>Editar {title}</h5>
    </div>
    <div class="card-body">
        <form method="POST">
            <!-- Agregar campos del formulario aquí -->
            
            <div class="d-flex justify-content-between">
                <a href="{{{{url_for('{module_name}.index') }}}}" class="btn btn-secondary">
                    <i class="bi bi-arrow-left"></i> Cancelar
                </a>
                <button type="submit" class="btn btn-primary">
                    <i class="bi bi-save"></i> Actualizar
                </button>
            </div>
        </form>
    </div>
</div>
{{%endblock %}}'''

def generate_detalle_template(module_name, title):
    return f'''{{%extends "base.html" %}}

{{%block title %}}Detalle {title} - Instituto Ballivián{{%endblock %}}
{{%block page_title %}}Detalle de {title}{{%endblock %}}

{{%block content %}}
<div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5>Información de {title}</h5>
        <div>
            {{%if current_user.tiene_permiso('editar_{module_name}') %}}
            <a href="{{{{url_for('{module_name}.editar', id=item.id) }}}}" class="btn btn-warning btn-sm">
                <i class="bi bi-pencil"></i> Editar
            </a>
            {{%endif %}}
            <a href="{{{{url_for('{module_name}.index') }}}}" class="btn btn-secondary btn-sm">
                <i class="bi bi-arrow-left"></i> Volver
            </a>
        </div>
    </div>
    <div class="card-body">
        <!-- Agregar detalles aquí -->
    </div>
</div>
{{%endblock %}}'''

def main():
    print("Generando estructura de templates...")
    create_directory_structure()
    
    print("\nGenerando archivos de templates...")
    
    for module, config in TEMPLATES.items():
        title = module.capitalize()
        
        templates_dir = f'templates/{module}'
        
        with open(f'{templates_dir}/index.html', 'w', encoding='utf-8') as f:
            f.write(generate_index_template(module, title))
        print(f"Creado: {templates_dir}/index.html")
        
        with open(f'{templates_dir}/crear.html', 'w', encoding='utf-8') as f:
            f.write(generate_crear_template(module, title, config['campos']))
        print(f"Creado: {templates_dir}/crear.html")
        
        with open(f'{templates_dir}/editar.html', 'w', encoding='utf-8') as f:
            f.write(generate_editar_template(module, title))
        print(f"Creado: {templates_dir}/editar.html")
        
        with open(f'{templates_dir}/detalle.html', 'w', encoding='utf-8') as f:
            f.write(generate_detalle_template(module, title))
        print(f"Creado: {templates_dir}/detalle.html")
    
    print("\n Generación de templates completada!")
    print("\n NOTA: Estos son templates base. Deberás personalizarlos según tus necesidades.")

if __name__ == '__main__':
    main()