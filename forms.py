from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=25), 
        Regexp(r'^[\w.@+-]+$', message="Username must contain only letters, numbers, and @/./+/-/_ characters.")
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    submit = SubmitField('Log In')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=25), 
        Regexp(r'^[\w.@+-]+$', message="Username must contain only letters, numbers, and @/./+/-/_ characters.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, max=128),
        Regexp(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
        )
    ])
    submit = SubmitField('Sign Up')