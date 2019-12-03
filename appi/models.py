from datetime import datetime
from appi import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from appi import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    rank = db.Column(db.String(64), default="General")
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    # Con esta funcion un usuario puede establecer una clave
    # convirtiendola a hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # Con esta funcion podemos saber si una clave es correcta 
    # usando solo el hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class DPGPAS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description =  db.Column(db.String(140))
    def __repr__(self):
        return '{}'.format(self.description)

class DSPGPGC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description =  db.Column(db.String(140))
    def __repr__(self):
        return '{}'.format(self.description)

class ProcessGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description =  db.Column(db.String(140))
    def __repr__(self):
        return '<Grupos de Procesos para Gestionar la Configuración del Sistem {}>'.format(self.description)

class ProcessGroupWithDPGPAS2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    process_id = db.Column(db.Integer, db.ForeignKey('process_group.id'))
    dpgpas_id = db.Column(db.Integer, db.ForeignKey('DPGPAS.id'))
    def __repr__(self):
        return '<Relación n a n de DPGPAS a ProcessGroup>'

class ProcessGroupWithDSPGPGC2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    process_id = db.Column(db.Integer, db.ForeignKey('process_group.id'))
    dspgpgc_id = db.Column(db.Integer, db.ForeignKey('DSPGPGC.id'))
    def __repr__(self):
        return '<Relación n a n de DSPGPGC a ProcessGroup>'

class Tec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('process_group.id'))
    description =  db.Column(db.String(140))
    def __repr__(self):
        return '<Tecnicas de los Grupos de Procesos {}>'.format(self.description)

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('process_group.id'))
    description =  db.Column(db.String(140))
    def __repr__(self):
        return '<Herramientas de los Grupos de Procesos {}>'.format(self.description)

class ParticipantsActors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('process_group.id'))
    name =  db.Column(db.String(140))
    lastname = db.Column(db.String(140))
    role = db.Column(db.String(64), default="Todos")
    def __repr__(self):
        return '<Actores Participantes de los Grupos de Procesos {}>'.format(self.description)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description =  db.Column(db.String(140))
    def __repr__(self):
        return '{}'.format(self.description)

class ActivityDPGPAS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('process_group.id'))
    dpgpas_id = db.Column(db.Integer, db.ForeignKey('process_group_with_dpgpa_s2.id'))
    description =  db.Column(db.String(140))
    def __repr__(self):
        return '{}'.format(self.description)

class ActivityDSPGPGC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('process_group.id'))
    dspgpgc_id = db.Column(db.Integer, db.ForeignKey('process_group_with_dspgpg_c2.id'))
    description =  db.Column(db.String(140))
    def __repr__(self):
        return '{}'.format(self.description)

class TaskActivityDPGPAS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('process_group.id'))
    dpgpas_id = db.Column(db.Integer, db.ForeignKey('process_group_with_dpgpa_s2.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activityDPGPAS.id'))
    description =  db.Column(db.String(140))
    def __repr__(self):
        return '{}'.format(self.description)


class TaskActivityDSPGPGC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey('process_group.id'))
    dspgpgc_id = db.Column(db.Integer, db.ForeignKey('process_group_with_dspgpg_c2.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activityDSPGPGC.id'))
    description =  db.Column(db.String(140))
    def __repr__(self):
        return '{}'.format(self.description)

