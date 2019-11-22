from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from appi.models import User, DPGPAS, DSPGPGC, Tec, Tool


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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

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

    def validate_description(self, description):
        query = DPGPAS.query.filter_by(description=description.data).first()
        if query is not None:
            raise ValidationError('Please use a different description.')

class EditFormDPGPAS(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit')


#DSPGPGC forms 

class RegistrationFormDSPGPGC(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_description(self, description):
        query = DSPGPGC.query.filter_by(description=description.data).first()
        if query is not None:
            raise ValidationError('Please use a different description.')

class EditFormDSPGPGC(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit')


#Tec forms 
class RegistrationFormTec(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_description(self, description):
        query = Tec.query.filter_by(description=description.data).first()
        if query is not None:
            raise ValidationError('Please use a different description.')

class EditFormTec(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit')

#Tool form
class RegistrationFormTool(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_description(self, description):
        query = Tool.query.filter_by(description=description.data).first()
        if query is not None:
            raise ValidationError('Please use a different description.')

class EditFormTool(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Edit')