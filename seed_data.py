from models import db, Usuario, Rol, Permiso, Persona, Estudiante, Docente, Carrera
from datetime import datetime, date

def init_data():
    
    # Verificar si ya existen datos
    if Usuario.query.first():
        print("Los datos ya existen. Omitiendo inicialización.")
        return
    
    print("Iniciando carga de datos de prueba...")
    
    # 1. Crear permisos
    permisos_data = [
        # Carreras
        ('ver_carreras', 'Puede ver carreras'),
        ('crear_carrera', 'Puede crear carreras'),
        ('editar_carrera', 'Puede editar carreras'),
        ('eliminar_carrera', 'Puede eliminar carreras'),
        # Materias
        ('ver_materias', 'Puede ver materias'),
        ('crear_materia', 'Puede crear materias'),
        ('editar_materia', 'Puede editar materias'),
        ('eliminar_materia', 'Puede eliminar materias'),
        # Personas
        ('ver_personas', 'Puede ver personas'),
        ('crear_persona', 'Puede crear personas'),
        ('editar_persona', 'Puede editar personas'),
        ('eliminar_persona', 'Puede eliminar personas'),
        # Estudiantes
        ('ver_estudiantes', 'Puede ver estudiantes'),
        ('crear_estudiante', 'Puede crear estudiantes'),
        ('editar_estudiante', 'Puede editar estudiantes'),
        ('eliminar_estudiante', 'Puede eliminar estudiantes'),
        # Docentes
        ('ver_docentes', 'Puede ver docentes'),
        ('crear_docente', 'Puede crear docentes'),
        ('editar_docente', 'Puede editar docentes'),
        ('eliminar_docente', 'Puede eliminar docentes'),
        # Asignaciones
        ('ver_asignaciones', 'Puede ver asignaciones'),
        ('crear_asignacion', 'Puede crear asignaciones'),
        ('editar_asignacion', 'Puede editar asignaciones'),
        ('eliminar_asignacion', 'Puede eliminar asignaciones'),
        # Inscripciones
        ('ver_inscripciones', 'Puede ver inscripciones'),
        ('crear_inscripcion', 'Puede crear inscripciones'),
        ('editar_inscripcion', 'Puede editar inscripciones'),
        ('eliminar_inscripcion', 'Puede eliminar inscripciones'),
        # Notas
        ('ver_notas', 'Puede ver notas'),
        ('crear_nota', 'Puede crear notas'),
        ('editar_nota', 'Puede editar notas'),
        ('eliminar_nota', 'Puede eliminar notas'),
        # Usuarios
        ('ver_usuarios', 'Puede ver usuarios'),
        ('crear_usuario', 'Puede crear usuarios'),
        ('editar_usuario', 'Puede editar usuarios'),
        ('eliminar_usuario', 'Puede eliminar usuarios'),
        # Roles
        ('ver_roles', 'Puede ver roles'),
        ('crear_rol', 'Puede crear roles'),
        ('editar_rol', 'Puede editar roles'),
        ('eliminar_rol', 'Puede eliminar roles'),
    ]
    
    permisos = {}
    for nombre, desc in permisos_data:
        permiso = Permiso(nombre=nombre, descripcion=desc)
        db.session.add(permiso)
        permisos[nombre] = permiso
    
    db.session.commit()
    print("Permisos creados.")
    
    rol_admin = Rol(nombre='Administrador', descripcion='Acceso total al sistema')
    rol_admin.permisos = list(permisos.values())
    db.session.add(rol_admin)
    
    rol_secretaria = Rol(nombre='Secretaria', descripcion='Gestión de estudiantes e inscripciones')
    rol_secretaria.permisos = [
        permisos['ver_carreras'], permisos['ver_materias'],
        permisos['ver_personas'], permisos['crear_persona'], permisos['editar_persona'],
        permisos['ver_estudiantes'], permisos['crear_estudiante'], permisos['editar_estudiante'],
        permisos['ver_docentes'],
        permisos['ver_inscripciones'], permisos['crear_inscripcion'], permisos['editar_inscripcion'],
        permisos['ver_asignaciones'],
    ]
    db.session.add(rol_secretaria)
    
    rol_docente = Rol(nombre='Docente', descripcion='Gestión de notas y visualización')
    rol_docente.permisos = [
        permisos['ver_carreras'], permisos['ver_materias'],
        permisos['ver_estudiantes'],
        permisos['ver_asignaciones'],
        permisos['ver_inscripciones'],
        permisos['ver_notas'], permisos['crear_nota'], permisos['editar_nota'],
    ]
    db.session.add(rol_docente)
    
    rol_estudiante = Rol(nombre='Estudiante', descripcion='Visualización de información académica')
    rol_estudiante.permisos = [
        permisos['ver_carreras'], permisos['ver_materias'],
        permisos['ver_inscripciones'], permisos['ver_notas'],
    ]
    db.session.add(rol_estudiante)
    
    db.session.commit()
    print("Roles creados.")
    
    persona_admin = Persona(
        tipo_documento='CI',
        nro_documento='1234567',
        nombre='Administrador',
        apellido_paterno='Sistema',
        apellido_materno='Principal',
        fecha_nacimiento=date(1990, 1, 1),
        sexo='M',
        email='admin@institutoballivian.edu.bo',
        telefono='70000000'
    )
    db.session.add(persona_admin)
    
    persona_secretaria = Persona(
        tipo_documento='CI',
        nro_documento='2345678',
        nombre='Maria',
        apellido_paterno='Gonzalez',
        apellido_materno='Lopez',
        fecha_nacimiento=date(1985, 5, 15),
        sexo='F',
        email='secretaria@institutoballivian.edu.bo',
        telefono='70111111'
    )
    db.session.add(persona_secretaria)
    
    persona_docente = Persona(
        tipo_documento='CI',
        nro_documento='3456789',
        nombre='Carlos',
        apellido_paterno='Rodriguez',
        apellido_materno='Martinez',
        fecha_nacimiento=date(1980, 3, 20),
        sexo='M',
        email='carlos.rodriguez@institutoballivian.edu.bo',
        telefono='70222222'
    )
    db.session.add(persona_docente)
    
    persona_estudiante = Persona(
        tipo_documento='CI',
        nro_documento='4567890',
        nombre='Ana',
        apellido_paterno='Perez',
        apellido_materno='Mamani',
        fecha_nacimiento=date(2000, 8, 10),
        sexo='F',
        email='ana.perez@estudiante.edu.bo',
        telefono='70333333'
    )
    db.session.add(persona_estudiante)
    
    db.session.commit()
    print("Personas creadas.")
    
    docente = Docente(
        persona_id=persona_docente.id,
        codigo_docente='DOC-001',
        grado_academico='Licenciatura',
        titulo_universitario='Licenciado en Informática',
        fecha_ingreso=date(2015, 1, 10),
        fecha_nacimiento=date(1980, 3, 20),
        activo=True
    )
    db.session.add(docente)
    db.session.commit()
    
    estudiante = Estudiante(
        persona_id=persona_estudiante.id,
        codigo_estudiante='EST-001',
        nacionalidad='Boliviana',
        departamento='La Paz',
        provincia='Murillo',
        estado_civil='Soltero',
        colegio_egreso='Colegio Bolívar',
        anio_egreso=2018,
        tipo_ingreso='Regular',
        activo=True
    )
    db.session.add(estudiante)
    db.session.commit()
    
    usuario_admin = Usuario(
        username='admin',
        email='admin@institutoballivian.edu.bo',
        persona_id=persona_admin.id,
        activo=True
    )
    usuario_admin.set_password('admin123')
    usuario_admin.roles.append(rol_admin)
    db.session.add(usuario_admin)
    
    usuario_secretaria = Usuario(
        username='secretaria',
        email='secretaria@institutoballivian.edu.bo',
        persona_id=persona_secretaria.id,
        activo=True
    )
    usuario_secretaria.set_password('secretaria123')
    usuario_secretaria.roles.append(rol_secretaria)
    db.session.add(usuario_secretaria)
    
    usuario_docente = Usuario(
        username='docente',
        email='carlos.rodriguez@institutoballivian.edu.bo',
        persona_id=persona_docente.id,
        docente_id=docente.id,
        activo=True
    )
    usuario_docente.set_password('docente123')
    usuario_docente.roles.append(rol_docente)
    db.session.add(usuario_docente)
    
    usuario_estudiante = Usuario(
        username='estudiante',
        email='ana.perez@estudiante.edu.bo',
        persona_id=persona_estudiante.id,
        estudiante_id=estudiante.id,
        activo=True
    )
    usuario_estudiante.set_password('estudiante123')
    usuario_estudiante.roles.append(rol_estudiante)
    db.session.add(usuario_estudiante)
    
    db.session.commit()
    print("Usuarios creados.")
    
    carreras_data = [
        ('ING-SIS', 'Ingeniería de Sistemas', 'Carrera de Ingeniería de Sistemas', 'Pregrado', 4800, 240),
        ('ING-IND', 'Ingeniería Industrial', 'Carrera de Ingeniería Industrial', 'Pregrado', 4800, 240),
        ('TEC-PROG', 'Técnico en Programación', 'Técnico Superior en Programación', 'Tecnico', 2400, 120),
    ]
    
    for codigo, nombre, desc, tipo, horas, creditos in carreras_data:
        carrera = Carrera(
            codigo=codigo,
            nombre=nombre,
            descripcion=desc,
            tipo=tipo,
            carga_horaria=horas,
            creditos=creditos,
            fecha_creacion=date(2020, 1, 1),
            activo=True
        )
        db.session.add(carrera)
    
    db.session.commit()
    print("Carreras creadas.")
    
    print("\n=== DATOS DE PRUEBA CARGADOS ===")
    print("\nUsuarios creados:")
    print("1. Admin: usuario='admin', password='admin123'")
    print("2. Secretaria: usuario='secretaria', password='secretaria123'")
    print("3. Docente: usuario='docente', password='docente123'")
    print("4. Estudiante: usuario='estudiante', password='estudiante123'")
    print("\n================================\n")