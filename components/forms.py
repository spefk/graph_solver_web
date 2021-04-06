from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import Field, StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, NoneOf, Optional, ValidationError
from wtforms_alchemy import ModelForm
from wtforms_alchemy.validators import Unique
from components.database_models import db, User


class RegisterForm(FlaskForm, ModelForm):
    username = StringField('New Username', validators=[InputRequired(message='Username is required'),
                                                       Length(min=4, max=20),
                                                       Unique(User.username, get_session=lambda: db.session,
                                                              message='Username is already taken.')])
    password = PasswordField('New Password', validators=[InputRequired(message='Password is required'),
                                                         EqualTo('password_conf', message='Passwords must match'),
                                                         Length(min=4, max=20)])
    password_conf = PasswordField('Repeat Password',
                                  validators=[InputRequired(message='Password validation is required'),
                                              Length(min=4, max=20)])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message='Username is required'),
                                                   Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(message='Password is required'),
                                                     Length(min=4, max=20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UploadGraphForm(FlaskForm):
    graph_name = StringField('Graph Name')
    graph = FileField('Graph (txt)', validators=[FileRequired(), FileAllowed(['txt', 'csv'])])
    submit = SubmitField('Upload')


class TSPForm(FlaskForm):
    select_graph = SelectField(u'Select an already downloaded graph')
    downloaded_graph = FileField('Or download a new one\n', validators=[FileAllowed(['txt', 'csv'])])


def cond_req_validator(cond_field_name, conditions=None):
    if conditions is None:
        conditions = []

    def _validator(form, field):
        print(field.data)
        print(type(field.data))
        print('here')
        print(field)
        if form[cond_field_name].data in conditions and field.data == "":
            raise ValidationError('Must be filled')

    return _validator


class APSPForm(FlaskForm):
    select_graph = SelectField(u'Select an already downloaded graph',
                               validators=[InputRequired(), NoneOf('...', message='Field is required.')])
    algorithm_mode = SelectField(u'Select problem to solve.', validators=[InputRequired()])
    s = StringField('Start', validators=[cond_req_validator('algorithm_mode', conditions=['1_to_1', '1_to_all'])])
    t = StringField('Destination', validators=[cond_req_validator('algorithm_mode',
                                                                  conditions=['1_to_1'])])


class MaxFlowForm(FlaskForm):
    select_graph = SelectField(u'Select an already downloaded graph',
                               validators=[InputRequired(), NoneOf('...', message='Field is required.')])
    algorithm = SelectField(u'Select algorithm to use.',
                            validators=[InputRequired(), NoneOf('...', message='Field is required.')])
    s = IntegerField('Source', validators=[InputRequired()])
    t = IntegerField('Sink', validators=[InputRequired()])
