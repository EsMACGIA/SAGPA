from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from appi.models import User, DPGPAS, DSPGPGC, Tec, Tool, ProcessGroup


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
    submit = SubmitField('Register')


class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    rank = SelectField(
        'User Rank',
        choices=[('General', 'General'), ('Administrator', 'Administrador'), ('Manager', 'Gerente')]
    )
    submit = SubmitField('Edit')

#DPGPAS forms 
class RegistrationFormDPGPAS(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditFormDPGPAS(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit')


#DSPGPGC forms 

class RegistrationFormDSPGPGC(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditFormDSPGPGC(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit')

# ProcessGroupWithDPGPAS2 form
class RegistrationFormProcessGroupWithDPGPAS2(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    discipline_id = QuerySelectField(query_factory=lambda: DPGPAS.query.all())
    submit = SubmitField('Register')

# ProcessGroupWithDPGPAS2 form
class RegistrationFormProcessGroupWithDSPGPGC2(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    discipline_id = QuerySelectField(query_factory=lambda: DSPGPGC.query.all())
    submit = SubmitField('Register')
class RegistrationFormProcessGroup(FlaskForm):
    description = StringField('Description',validators=[DataRequired()])
    SubmitField = SubmitField('Register')

class EditFormProcessGroup(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit')

#Tec forms 
class RegistrationFormTec(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditFormTec(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit')

#Tool form
class RegistrationFormTool(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditFormTool(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit')

#Participants Actors

class RegistrationFormActor(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    lastname = StringField('Lastname',validators=[DataRequired()])
    role = SelectField(
        'Actor Role',
        choices=[('Todos', 'Todos'), ('Gcia Agropecuaria', 'Gcia Agropecuaria'), ('Gcia Ganaderia', 'Gcia Ganaderia'), ('Gcia Agricola', 'Gcia Agricola')]
    )
    submit = SubmitField('Register')
