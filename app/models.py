from datetime import datetime
from flask_bcrypt import Bcrypt
from . import db

bcrypt = Bcrypt()

# Modelo para el usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable = False)
    roles = db.relationship('Role', secondary='user_roles')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Modelo para los roles
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


# Tabla intermedia para muchos a muchos entre usuarios y roles
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=False)

class Transcripcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    palabras_clave = db.Column(db.String, nullable = True)
    descripcion = db.Column(db.String, nullable = True)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesion.id'), nullable = False)


class Resumen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesion.id'), nullable = False)
    resumen_general = db.Column(db.String, nullable = True)
    proposito_clase = db.Column(db.String, nullable = True)
    inicio = db.Column(db.String, nullable = True)
    desarrollo = db.Column(db.String, nullable = True)
    cierre = db.Column(db.String, nullable = True)

class Rubrica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    factores = db.Column(db.String, nullable = True)
    criterios = db.Column(db.String, nullable = True)
    items = db.Column(db.String, nullable = True)

class ResultadoRubrica(db.Model):
    __tablename__ = 'resultado_rubrica'
    id = db.Column(db.Integer, primary_key=True)
    cumple_satis = db.Column(db.String, nullable = True)
    cumple = db.Column(db.String, nullable = True)
    cumple_parcial = db.Column(db.String, nullable = True)
    cumple_no = db.Column(db.String, nullable = True)
    id_rubrica = db.Column(db.Integer, db.ForeignKey('rubrica.id'), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesion.id'), nullable = False)

class Sesion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable = True)
    institucion = db.Column(db.String, nullable = True)
    fecha_dictada = db.Column(db.Date, nullable = True)
    duracion_video = db.Column(db.Numeric(3,2), nullable = True)
    fecha_creacion = db.Column(db.Date, nullable = True)
    descripcion = db.Column(db.String, nullable = True)
    grabacion = db.Column(db.String, nullable = True)
    auditado = db.Column(db.Boolean, default=False, nullable = True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    observacion = db.Column(db.String, nullable = True)
    hallazgos = db.Column(db.String, nullable = True)
    recomendacion = db.Column(db.String, nullable = True)
    fecha_feedback = db.Column(db.Date, nullable = True)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesion.id'), nullable = False)


class AnalisisModelo(db.Model):
    __tablename__ = 'analisis_modelo'
    id = db.Column(db.Integer, primary_key=True)
    id_transcripcion = db.Column(db.Integer, db.ForeignKey('transcripcion.id'), nullable = False)
    id_resumen = db.Column(db.Integer, db.ForeignKey('resumen.id'), nullable = False)
    id_resultado_rubrica = db.Column(db.Integer, db.ForeignKey('resultado_rubrica.id'), nullable = False)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesion.id'), nullable = False)
    id_feedback = db.Column(db.Integer, db.ForeignKey('feedback.id'), nullable = False)

