from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
from werkzeug.security import check_password_hash
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password must match!')])
    # role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    role = StringField('Role', default='User')
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not check_password_hash(user.password, field.data):
            raise ValidationError('Incorrect password')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = CKEditorField('Description')
    deadline = DateTimeLocalField('Deadline', format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Submit')