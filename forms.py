from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, DecimalField, URLField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, URL
import html
from datetime import datetime

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

class TwoFactorForm(FlaskForm):
    token = StringField('2FA Token', validators=[DataRequired()])
    submit = SubmitField('Verify')

class LogEntryForm(FlaskForm):
    developer = StringField('Developer', validators=[DataRequired(), Length(max=50)], render_kw={'readonly': True})
    project = StringField('Project', validators=[DataRequired(), Length(max=100)])
    start_time = DateTimeField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    time_worked = DecimalField('Time Worked (hours)', places=2, validators=[DataRequired()])
    repo = URLField('Repo Link', validators=[DataRequired(), URL()])
    developer_notes = TextAreaField('Developer Notes', validators=[Length(max=500)])
    developer_code = TextAreaField('Developer Code', validators=[DataRequired(), Length(max=1000)])
    diary_entry = HiddenField('Timestamp', default=datetime.utcnow().isoformat())
    submit = SubmitField('Submit')

    def __init__(self, username=None, *args, **kwargs):
        super(LogEntryForm, self).__init__(*args, **kwargs)
        if username:
            self.developer.data = username
    
    def sanitizeLogData(self):
        self.developer.data = html.escape(self.developer.data)
        self.project.data = html.escape(self.project.data)
        self.repo.data = html.escape(self.repo.data)
        self.developer_notes.data = html.escape(self.developer_notes.data)
        self.developer_code.data = html.escape(self.developer_code.data)

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete my Data')