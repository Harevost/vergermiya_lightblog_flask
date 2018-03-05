from flask_wtf import Form
from wtforms import (StringField, TextField, TextAreaField, PasswordField,
                      BooleanField, ValidationError)
from wtforms.validators import DataRequired, Length, EqualTo, URL

from vergermiya_lightblog.models import User


class LoginForm(Form):
    """
    Login Form validator
    """
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])

    def validate(self):
        """Validator for check the account information."""
        is_validated = super(LoginForm, self).validate()

        if not is_validated:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False

        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password.')
            return False

        return True


class RegisterForm(Form):
    """
    Register Form
    """
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])

    def validate(self):
        is_validated = super(RegisterForm, self).validate()

        if not is_validated:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User already exists.')
            return False
        return True


class PostForm(Form):
    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Blog Content', [DataRequired()])


class CommentForm(Form):
    """
    Comment Form validator
    """
    name = StringField("name", validators=[DataRequired(), Length(max=255)])
    text = StringField("Comment", validators=[DataRequired()])

