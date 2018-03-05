from flask_wtf import Form
from wtforms import StringField, TextField
from wtforms.validators import DataRequired, Length


class CommentForm(Form):
    """
    Comment Form vaildator
    """
    name = StringField("name", validators=[DataRequired(), Length(max=255)])
    text = StringField("Comment", validators=[DataRequired()])

