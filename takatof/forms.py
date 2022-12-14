from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, AnyOf
from takatof.config import BUILDING_ROOM_LIST
from takatof.models import getBuildingList

class PostForm(FlaskForm):
    room_number = SelectField("Room Number", choices=BUILDING_ROOM_LIST, validators=[DataRequired(), AnyOf(values=BUILDING_ROOM_LIST)])
    content = TextAreaField("Content", render_kw={"placeholder": "ورق بلوت، طقم مفكات، فلاتر قهوة، اللي ودك!"}, validators=[DataRequired(), Length(min=1, max=140)])
    note = TextAreaField("Note", render_kw={"placeholder": "تعال بعد المغرب، قبل 12، اللي يناسبك!"}, validators=[Length(max=140)])
    submit = SubmitField("إضافة")

class SearchForm(FlaskForm):
    building = SelectField(choices=getBuildingList(), validators=[DataRequired(), AnyOf(values=getBuildingList())])
    submit = SubmitField("بحث")

class ReportForm(FlaskForm):
    submit = SubmitField("تأكيد")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("دخول")
