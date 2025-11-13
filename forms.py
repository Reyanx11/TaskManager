from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField,DateTimeLocalField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateTimeLocalField('Due Date', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    priority = SelectField('Priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    submit = SubmitField('Add Task')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    submit = SubmitField('Update Profile')