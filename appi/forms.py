from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from appi.models import User, DPGPAS, DSPGPGC, Tec, Tool, ProcessGroup, Project


#Users Forms

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')


class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    rank = SelectField(
        'User Rank',
        choices=[('General', 'General'), ('Administrator', 'Administrador'), ('Manager', 'Gerente'), ('Specialist', 'Especialista')]
    )
    project_id = QuerySelectField('Proyecto', query_factory=lambda: Project.query.all(), default=None)
    submit = SubmitField('Editar')

#DPGPAS forms 
class RegistrationFormDPGPAS(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class EditFormDPGPAS(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Editar')


#DSPGPGC forms 

class RegistrationFormDSPGPGC(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class EditFormDSPGPGC(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Editar')

# ProcessGroupWithDPGPAS2 form
class RegistrationFormProcessGroupWithDPGPAS2(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    discipline_id = QuerySelectField(query_factory=lambda: DPGPAS.query.all())
    submit = SubmitField('Registrar')

# ProcessGroupWithDPGPAS2 form
class RegistrationFormProcessGroupWithDSPGPGC2(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    discipline_id = QuerySelectField(query_factory=lambda: DSPGPGC.query.all())
    submit = SubmitField('Registrar')
    
class RegistrationFormProcessGroup(FlaskForm):
    description = StringField('Description',validators=[DataRequired()])
    SubmitField = SubmitField('Registrar')

class EditFormProcessGroup(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Editar')

#Tec forms 
class RegistrationFormTec(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class EditFormTec(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Editar')

#Tool form
class RegistrationFormTool(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class EditFormTool(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Editar')

#Participants Actors

class RegistrationFormActor(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    lastname = StringField('Lastname',validators=[DataRequired()])
    role = SelectField(
        'Actor Role',
        choices=[('Todos', 'Todos'), ('Gcia Agropecuaria', 'Gcia Agropecuaria'), ('Gcia Ganaderia', 'Gcia Ganaderia'), ('Gcia Agricola', 'Gcia Agricola')]
    )
    submit = SubmitField('Registrar')

#Project

class RegistrationFormProject(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def validate_description(self, description):
        query = DSPGPGC.query.filter_by(description=description.data).first()
        if query is not None:
            raise ValidationError('Please use a different description.')

class EditFormProject(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Editar')

# DPGPAS Activities

class RegistrationFormDPGPASActivity(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class EditFormDPGPASActivity(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Editar')

# DSPGPGC Activities

class RegistrationFormDSPGPGCActivity(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class EditFormDSPGPGCActivity(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Editar')

# Task DPGPAS Activities

class RegistrationFormTaskDPGPASActivities(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class EditFormTaskDPGPASActivities(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Editar')

# Task DPGPAS Activities

class RegistrationFormTaskDPGPASActivities(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class EditFormTaskDSPGPGCActivities(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Editar')