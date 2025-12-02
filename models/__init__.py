from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

usuario_rol = db.Table('usuario_rol',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'), primary_key=True),
    db.Column('asignado_en', db.DateTime, default=datetime.utcnow)
)

rol_permiso = db.Table('rol_permiso',
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'), primary_key=True),
    db.Column('permiso_id', db.Integer, db.ForeignKey('permiso.id'), primary_key=True)
)

# Modelos
class Carrera(db.Model):
    __tablename__ = 'carrera'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.Enum('Pregrado', 'Tecnico', 'Posgrado', 'Diplomado', 'Otro'), default='Pregrado')
    carga_horaria = db.Column(db.Integer, default=0)
    creditos = db.Column(db.Integer)
    fecha_creacion = db.Column(db.Date)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relaciones
    materias = db.relationship('Materia', backref='carrera', lazy=True, cascade='all, delete-orphan')
    inscripciones = db.relationship('Inscripcion', backref='carrera', lazy=True)
    asignaciones = db.relationship('Asignacion', backref='carrera', lazy=True)
    
    def __repr__(self):
        return f'<Carrera {self.nombre}>'

class Materia(db.Model):
    __tablename__ = 'materia'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    carga_horaria = db.Column(db.Integer, default=0)
    horas_teoricas = db.Column(db.Integer, default=0)
    horas_practicas = db.Column(db.Integer, default=0)
    creditos = db.Column(db.Integer, default=0)
    semestre = db.Column(db.Integer)
    prerequisito_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'))
    requerido_para_semestre = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relaciones
    asignaciones = db.relationship('Asignacion', backref='materia', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Materia {self.nombre}>'

class Persona(db.Model):
    __tablename__ = 'persona'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo_documento = db.Column(db.Enum('CI', 'Pasaporte', 'Otro'), default='CI')
    nro_documento = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    sexo = db.Column(db.Enum('M', 'F', 'O'))
    lugar_nacimiento = db.Column(db.String(255))
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(150))
    foto_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('tipo_documento', 'nro_documento', name='_tipo_nro_uc'),
    )
    
    # Relaciones
    estudiante = db.relationship('Estudiante', backref='persona', uselist=False, cascade='all, delete-orphan')
    docente = db.relationship('Docente', backref='persona', uselist=False, cascade='all, delete-orphan')
    usuario = db.relationship('Usuario', backref='persona', uselist=False)
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno or ''}".strip()
    
    def __repr__(self):
        return f'<Persona {self.nombre_completo}>'

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)
    codigo_estudiante = db.Column(db.String(50), unique=True)
    nacionalidad = db.Column(db.String(100))
    provincia = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    estado_civil = db.Column(db.Enum('Soltero', 'Casado', 'Viudo', 'Divorciado', 'Otro'), default='Soltero')
    idioma_orig = db.Column(db.String(50))
    comunidad = db.Column(db.String(100))
    zona = db.Column(db.String(100))
    colegio_egreso = db.Column(db.String(255))
    anio_egreso = db.Column(db.Integer)
    tipo_ingreso = db.Column(db.Enum('Regular', 'Traslado', 'Libre'), default='Regular')
    foto_path = db.Column(db.String(500))
    record_academico_path = db.Column(db.String(500))
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relaciones
    inscripciones = db.relationship('Inscripcion', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    registros = db.relationship('Registro', backref='estudiante', lazy=True)
    usuario = db.relationship('Usuario', backref='estudiante', uselist=False)
    
    def __repr__(self):
        return f'<Estudiante {self.codigo_estudiante}>'

class Docente(db.Model):
    __tablename__ = 'docente'
    
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)
    codigo_docente = db.Column(db.String(50), unique=True)
    grado_academico = db.Column(db.String(150))
    fecha_ingreso = db.Column(db.Date)
    fecha_nacimiento = db.Column(db.Date)
    titulo_universitario = db.Column(db.String(255))
    foto_path = db.Column(db.String(500))
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relaciones
    asignaciones = db.relationship('Asignacion', backref='docente', lazy=True, cascade='all, delete-orphan')
    usuario = db.relationship('Usuario', backref='docente', uselist=False)
    
    def __repr__(self):
        return f'<Docente {self.codigo_docente}>'

class AcademicSystem(db.Model):
    __tablename__ = 'academic_system'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), default='Instituto Ballivian')
    gestion = db.Column(db.Integer)
    periodo = db.Column(db.Enum('I', 'II', 'III', 'Cuatrimestral', 'Otro'))
    descripcion = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AcademicSystem {self.nombre}>'

class Asignacion(db.Model):
    __tablename__ = 'asignacion'
    
    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docente.id'), nullable=False)
    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'))
    gestion = db.Column(db.Integer, nullable=False)
    periodo = db.Column(db.Enum('I', 'II', 'III', 'Cuatrimestral', 'Anual'), default='I')
    codigo_grupo = db.Column(db.String(50))
    horario = db.Column(db.Text)
    tipo_imparticion = db.Column(db.Enum('Presencial', 'Virtual', 'Hibrido'), default='Presencial')
    cupo = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relaciones
    notas = db.relationship('Nota', backref='asignacion', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Asignacion {self.codigo_grupo}>'

class Inscripcion(db.Model):
    __tablename__ = 'inscripcion'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)
    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'), nullable=False)
    gestion = db.Column(db.Integer, nullable=False)
    periodo = db.Column(db.Enum('I', 'II', 'III', 'Cuatrimestral', 'Anual'), default='I')
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Enum('Preinscrito', 'Matriculado', 'Rechazado', 'Anulado'), default='Matriculado')
    metodo_ingreso = db.Column(db.Enum('Regular', 'Traslado', 'Admitido', 'Otro'), default='Regular')
    boletin_id = db.Column(db.Integer)
    formulario_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relaciones
    depositos = db.relationship('DepositoBancario', backref='inscripcion', lazy=True, cascade='all, delete-orphan')
    boletas = db.relationship('BoletaInscripcion', backref='inscripcion', lazy=True, cascade='all, delete-orphan')
    notas = db.relationship('Nota', backref='inscripcion', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Inscripcion {self.id}>'

class DepositoBancario(db.Model):
    __tablename__ = 'deposito_bancario'
    
    id = db.Column(db.Integer, primary_key=True)
    inscripcion_id = db.Column(db.Integer, db.ForeignKey('inscripcion.id'), nullable=False)
    banco = db.Column(db.String(150))
    monto = db.Column(db.Numeric(12, 2), default=0.00)
    fecha_deposito = db.Column(db.Date)
    nro_deposito = db.Column(db.String(100))
    comprobante_path = db.Column(db.String(500))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DepositoBancario {self.nro_deposito}>'

class BoletaInscripcion(db.Model):
    __tablename__ = 'boleta_inscripcion'
    
    id = db.Column(db.Integer, primary_key=True)
    inscripcion_id = db.Column(db.Integer, db.ForeignKey('inscripcion.id'), nullable=False)
    gestion = db.Column(db.Integer, nullable=False)
    periodo = db.Column(db.Enum('I', 'II', 'III', 'Cuatrimestral', 'Anual'), default='I')
    fecha_emision = db.Column(db.DateTime, default=datetime.utcnow)
    monto_total = db.Column(db.Numeric(12, 2), default=0.00)
    detalles = db.Column(db.Text)
    archivo_path = db.Column(db.String(500))
    
    def __repr__(self):
        return f'<BoletaInscripcion {self.id}>'

class Nota(db.Model):
    __tablename__ = 'nota'
    
    id = db.Column(db.Integer, primary_key=True)
    inscripcion_id = db.Column(db.Integer, db.ForeignKey('inscripcion.id'), nullable=False)
    asignacion_id = db.Column(db.Integer, db.ForeignKey('asignacion.id'), nullable=False)
    primer_parcial = db.Column(db.Numeric(5, 2))
    segundo_parcial = db.Column(db.Numeric(5, 2))
    tercer_parcial = db.Column(db.Numeric(5, 2))
    nota_final = db.Column(db.Numeric(5, 2))
    promedio = db.Column(db.Numeric(5, 2))
    observaciones = db.Column(db.Text)
    estado = db.Column(db.Enum('Abierto', 'Cerrado', 'Revisado'), default='Abierto')
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_update = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Nota {self.id}>'

class Registro(db.Model):
    __tablename__ = 'registro'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id'))
    tipo_registro = db.Column(db.Enum('Matricula', 'Inscripcion', 'Cambio', 'Baja', 'RegistroNotas', 'Otro'), default='Otro')
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer)
    referencia_id = db.Column(db.Integer)
    
    # Relaciones
    hojas = db.relationship('HojaRegistro', backref='registro', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Registro {self.tipo_registro}>'

class HojaRegistro(db.Model):
    __tablename__ = 'hoja_registro'
    
    id = db.Column(db.Integer, primary_key=True)
    registro_id = db.Column(db.Integer, db.ForeignKey('registro.id'), nullable=False)
    documento_path = db.Column(db.String(500))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<HojaRegistro {self.id}>'

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150))
    password_hash = db.Column(db.String(255), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'))
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id'))
    docente_id = db.Column(db.Integer, db.ForeignKey('docente.id'))
    activo = db.Column(db.Boolean, default=True)
    ultimo_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relaciones
    roles = db.relationship('Rol', secondary=usuario_rol, backref='usuarios')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def tiene_permiso(self, nombre_permiso):
        for rol in self.roles:
            for permiso in rol.permisos:
                if permiso.nombre == nombre_permiso:
                    return True
        return False
    
    def tiene_rol(self, nombre_rol):
        return any(rol.nombre == nombre_rol for rol in self.roles)
    
    def __repr__(self):
        return f'<Usuario {self.username}>'

class Rol(db.Model):
    __tablename__ = 'rol'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    permisos = db.relationship('Permiso', secondary=rol_permiso, backref='roles')
    
    def __repr__(self):
        return f'<Rol {self.nombre}>'

class Permiso(db.Model):
    __tablename__ = 'permiso'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Permiso {self.nombre}>'

class Reporte(db.Model):
    __tablename__ = 'reporte'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.Enum('Notas', 'HistorialAcademico', 'DocentesPorIngreso', 'Matriculas', 'Otro'), default='Otro')
    parametro = db.Column(db.JSON)
    creado_por = db.Column(db.Integer)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    generados = db.relationship('ReporteGenerado', backref='reporte', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Reporte {self.nombre}>'

class ReporteGenerado(db.Model):
    __tablename__ = 'reporte_generado'
    
    id = db.Column(db.Integer, primary_key=True)
    reporte_id = db.Column(db.Integer, db.ForeignKey('reporte.id'), nullable=False)
    generado_por = db.Column(db.Integer)
    parametros = db.Column(db.JSON)
    archivo_path = db.Column(db.String(500))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ReporteGenerado {self.id}>'
    






    