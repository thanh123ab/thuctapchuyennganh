from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Tên', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Xác nhận mật khẩu', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Đăng ký')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')

class EventForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()])
    description = TextAreaField('Mô tả', validators=[Optional()])
    start = DateTimeField('Bắt đầu', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end = DateTimeField('Kết thúc', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    reminder_minutes_before = IntegerField('Nhắc trước (phút)', default=0, validators=[Optional()])
    repeat_type = SelectField('Lặp lại', choices=[
        ('none', 'Không lặp'),
        ('daily', 'Hàng ngày'),
        ('weekly', 'Hàng tuần'),
        ('monthly', 'Hàng tháng')
    ], default='none')
    submit = SubmitField('Lưu')

# Thêm form để admin chỉnh sửa người dùng
class AdminUserForm(FlaskForm):
    name = StringField('Tên người dùng', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu (chỉ điền khi cần đổi)')
    is_admin = BooleanField('Là quản trị viên')
    submit = SubmitField('Lưu')

#  Thêm form để admin quản lý sự kiện
class AdminEventForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()])
    description = TextAreaField('Mô tả', validators=[Optional()])
    start = DateTimeField('Bắt đầu', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end = DateTimeField('Kết thúc', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    reminder_minutes_before = IntegerField('Nhắc trước (phút)', default=0, validators=[Optional()])
    repeat_type = SelectField('Lặp lại', choices=[
        ('none', 'Không lặp'),
        ('daily', 'Hàng ngày'),
        ('weekly', 'Hàng tuần'),
        ('monthly', 'Hàng tháng')
    ], default='none')
    user_id = IntegerField('ID Người dùng', validators=[DataRequired()])
    submit = SubmitField('Lưu')

class SettingForm(FlaskForm):
    key = StringField('Khóa cấu hình', validators=[DataRequired()])
    value = StringField('Giá trị', validators=[DataRequired()])
    description = TextAreaField('Mô tả')
    submit = SubmitField('Lưu')
