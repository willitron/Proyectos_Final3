from faker import Faker
import random
from datetime import date
from sqlalchemy import text
from app import create_app
from models import db, Usuario, Rol, Permiso, Persona, Estudiante, Docente, Carrera, Materia, Asignacion, Inscripcion

fake = Faker(['es_ES'])

N_ESTUDIANTES = 40
N_DOCENTES = 18
N_SECRETARIAS = 2
MATERIAS_POR_CARRERA = 6
DEFAULT_PASS = 'Password2025'

CARRERAS = [
    'Ingeniería de Sistemas', 'Administración de Empresas', 'Contabilidad',
    'Electrónica', 'Enfermería', 'Arquitectura', 'Derecho', 'Turismo'
]

def generar_ci():
    return str(random.randint(1000000, 99999999))

def generar_telefono():
    return str(random.choice([6,7])) + ''.join(str(random.randint(0,9)) for _ in range(7))

def email_from_name(nombre, apellido):
    local = f"{nombre}.{apellido}".lower().replace(' ', '')
    dominio = random.choice(['institutoballivian.edu.bo', 'estudiante.edu.bo', 'docente.edu.bo'])
    return f"{local}@{dominio}"

def init_data():
    app = create_app()
    with app.app_context():
        print('Borrando y creando tablas...')
        db.drop_all()
        db.create_all()

        print('Creando permisos...')
        permisos_lista = [
            'ver_carreras','crear_carrera','editar_carrera','eliminar_carrera',
            'ver_materias','crear_materia','editar_materia','eliminar_materia',
            'ver_personas','crear_persona','editar_persona','eliminar_persona',
            'ver_estudiantes','crear_estudiante','editar_estudiante','eliminar_estudiante',
            'ver_docentes','crear_docente','editar_docente','eliminar_docente',
            'ver_asignaciones','crear_asignacion','editar_asignacion','eliminar_asignacion',
            'ver_inscripciones','crear_inscripcion','editar_inscripcion','eliminar_inscripcion',
            'ver_notas','crear_nota','editar_nota','eliminar_nota',
            'ver_usuarios','crear_usuario','editar_usuario','eliminar_usuario',
            'ver_roles','crear_rol','editar_rol','eliminar_rol'
        ]

        permisos = {}
        for p in permisos_lista:
            obj = Permiso(nombre=p, descripcion=f'Permiso {p}')
            db.session.add(obj)
            permisos[p] = obj
        db.session.commit()
        print(f'  Permisos creados: {len(permisos)}')

        print('Creando roles...')
        rol_admin = Rol(nombre='Administrador', descripcion='Acceso total')
        rol_admin.permisos = list(permisos.values())
        db.session.add(rol_admin)

        rol_secretaria = Rol(nombre='Secretaria', descripcion='Gestiona inscripciones y datos')
        rol_secretaria.permisos = [permisos[k] for k in [
            'ver_carreras','ver_materias','ver_personas','crear_persona','editar_persona',
            'ver_estudiantes','crear_estudiante','editar_estudiante','ver_inscripciones','crear_inscripcion'
        ]]
        db.session.add(rol_secretaria)

        rol_docente = Rol(nombre='Docente', descripcion='Docente del instituto')
        rol_docente.permisos = [permisos[k] for k in [
            'ver_materias','ver_estudiantes','ver_asignaciones','ver_notas','crear_nota','editar_nota'
        ]]
        db.session.add(rol_docente)

        rol_estudiante = Rol(nombre='Estudiante', descripcion='Acceso a su información')
        rol_estudiante.permisos = [permisos[k] for k in [
            'ver_carreras','ver_materias','ver_inscripciones','ver_notas'
        ]]
        db.session.add(rol_estudiante)

        db.session.commit()
        print('  Roles creados.')

        print('Creando carreras y materias...')
        carreras_objs = []
        for idx, cname in enumerate(CARRERAS, start=1):
            carrera = Carrera(
                codigo=f'C{100+idx}',
                nombre=cname,
                descripcion=f'Carrera de {cname}',
                tipo='Pregrado',
                carga_horaria=4800,
                creditos=240,
                fecha_creacion=date(2020,1,1),
                activo=True
            )
            db.session.add(carrera)
            carreras_objs.append(carrera)
        db.session.commit()

        materias_objs = []
        for carrera in carreras_objs:
            for m in range(1, MATERIAS_POR_CARRERA + 1):
                codigo = f"{carrera.codigo}-M{m:02d}"
                materia = Materia(
                    codigo=codigo,
                    nombre=f'Materia {m} - {carrera.nombre}',
                    descripcion=f'Materia {m} de {carrera.nombre}',
                    carga_horaria=48,
                    horas_teoricas=32,
                    horas_practicas=16,
                    creditos=4,
                    semestre=((m-1) % 8) + 1,
                    carrera_id=carrera.id,
                    activo=True
                )
                db.session.add(materia)
                materias_objs.append(materia)
        db.session.commit()
        print(f'  Carreras: {len(carreras_objs)}; Materias: {len(materias_objs)}')

        print('Creando docentes...')
        docentes_objs = []
        for i in range(N_DOCENTES):
            nombre = fake.first_name()
            apellido = fake.last_name()
            persona = Persona(
                tipo_documento='CI',
                nro_documento=generar_ci(),
                nombre=nombre,
                apellido_paterno=apellido,
                apellido_materno=fake.last_name(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=30, maximum_age=65),
                sexo=random.choice(['M','F']),
                direccion=fake.address(),
                telefono=generar_telefono(),
                email=email_from_name(nombre, apellido)
            )
            db.session.add(persona)
            db.session.flush()

            docente = Docente(
                persona_id=persona.id,
                codigo_docente=f'DOC-{1000+i}',
                grado_academico=random.choice(['Licenciado','Magister','Doctor']),
                fecha_ingreso=fake.date_between(start_date='-10y', end_date='today'),
                fecha_nacimiento=persona.fecha_nacimiento,
                titulo_universitario=random.choice(['Licenciado en Informática','Ingeniero','Licenciado en Educación']),
                activo=True
            )
            db.session.add(docente)
            db.session.flush()

            usuario = Usuario(
                username=f'docente{i+1}',
                email=persona.email,
                persona_id=persona.id,
                docente_id=docente.id,
                activo=True
            )
            usuario.set_password(DEFAULT_PASS)
            usuario.roles.append(Rol.query.filter_by(nombre='Docente').first())
            db.session.add(usuario)

            docentes_objs.append(docente)
        db.session.commit()
        print(f'  Docentes creados: {len(docentes_objs)}')

        print('Creando estudiantes...')
        estudiantes_objs = []
        for i in range(N_ESTUDIANTES):
            nombre = fake.first_name()
            apellido = fake.last_name()
            persona = Persona(
                tipo_documento='CI',
                nro_documento=generar_ci(),
                nombre=nombre,
                apellido_paterno=apellido,
                apellido_materno=fake.last_name(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=17, maximum_age=35),
                sexo=random.choice(['M','F']),
                direccion=fake.address(),
                telefono=generar_telefono(),
                email=email_from_name(nombre, apellido)
            )
            db.session.add(persona)
            db.session.flush()

            estudiante = Estudiante(
                persona_id=persona.id,
                codigo_estudiante=f'EST-{2000+i}',
                nacionalidad='Boliviana',
                provincia=fake.state(),
                departamento=fake.state(),
                estado_civil='Soltero',
                colegio_egreso=fake.company(),
                anio_egreso=random.randint(2005, 2024),
                tipo_ingreso='Regular',
                activo=True
            )
            db.session.add(estudiante)
            db.session.flush()

            usuario = Usuario(
                username=f'estudiante{i+1}',
                email=persona.email,
                persona_id=persona.id,
                estudiante_id=estudiante.id,
                activo=True
            )
            usuario.set_password(DEFAULT_PASS)
            usuario.roles.append(Rol.query.filter_by(nombre='Estudiante').first())
            db.session.add(usuario)

            estudiantes_objs.append(estudiante)
        db.session.commit()
        print(f'  Estudiantes creados: {len(estudiantes_objs)}')

        print('Creando secretarias...')
        secretarias = []
        for i in range(N_SECRETARIAS):
            nombre = fake.first_name()
            apellido = fake.last_name()
            persona = Persona(
                tipo_documento='CI',
                nro_documento=generar_ci(),
                nombre=nombre,
                apellido_paterno=apellido,
                apellido_materno=fake.last_name(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=25, maximum_age=60),
                sexo=random.choice(['M','F']),
                direccion=fake.address(),
                telefono=generar_telefono(),
                email=f'secretaria{i+1}@institutoballivian.edu.bo'
            )
            db.session.add(persona)
            db.session.flush()

            usuario = Usuario(
                username=f'secretaria{i+1}',
                email=persona.email,
                persona_id=persona.id,
                activo=True
            )
            usuario.set_password('secretaria123')
            usuario.roles.append(Rol.query.filter_by(nombre='Secretaria').first())
            db.session.add(usuario)
            secretarias.append(usuario)
        db.session.commit()
        print(f'  Secretarias creadas: {len(secretarias)}')

        print('Creando asignaciones...')
        asignaciones = []
        materias_all = Materia.query.all()
        for materia in materias_all:
            docente = random.choice(docentes_objs)
            asignacion = Asignacion(
                materia_id=materia.id,
                docente_id=docente.id,
                carrera_id=materia.carrera_id,
                gestion=random.randint(2020, 2025),
                periodo=random.choice(['I','II','III','Cuatrimestral','Anual']),
                codigo_grupo=f'G-{random.randint(1,6)}',
                horario='Lun/Mie 08:00-10:00',
                tipo_imparticion='Presencial',
                cupo=30
            )
            db.session.add(asignacion)
            asignaciones.append(asignacion)
        db.session.commit()
        print(f'  Asignaciones creadas: {len(asignaciones)}')

        print('Inscribiendo estudiantes...')
        inscripciones = []
        for est in estudiantes_objs:
            carrera = random.choice(carreras_objs)
            ins = Inscripcion(
                estudiante_id=est.id,
                carrera_id=carrera.id,
                gestion=random.randint(2020, 2025),
                periodo=random.choice(['I','II','III','Cuatrimestral','Anual']),
                estado='Matriculado'
            )
            db.session.add(ins)
            inscripciones.append(ins)
        db.session.commit()
        print(f'  Inscripciones creadas: {len(inscripciones)}')

        print('Creando usuario administrador...')
        persona_admin = Persona(
            tipo_documento='CI', nro_documento='1000000',
            nombre='Admin', apellido_paterno='Sistema', apellido_materno='Principal',
            fecha_nacimiento=date(1990,1,1), sexo='M',
            email='admin@institutoballivian.edu.bo', telefono='70000000'
        )
        db.session.add(persona_admin)
        db.session.flush()

        usuario_admin = Usuario(username='admin', email=persona_admin.email, persona_id=persona_admin.id, activo=True)
        usuario_admin.set_password('admin123')
        usuario_admin.roles.append(Rol.query.filter_by(nombre='Administrador').first())
        db.session.add(usuario_admin)
        db.session.commit()

        print('Seed completado con éxito!')

if __name__ == '__main__':
    init_data()
