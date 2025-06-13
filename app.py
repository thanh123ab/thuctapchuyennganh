from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Event, Log
from forms import RegisterForm, LoginForm, EventForm
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from email_service import mail
from reminder_scheduler import start_reminder_scheduler

app = Flask(__name__)
app.config.from_object(Config)
mail.init_app(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(func):
    @login_required
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)

    decorated_view.__name__ = func.__name__
    return decorated_view


@app.route('/get_events')
def get_events():
    events = Event.query.all()
    event_list = []
    for event in events:
        event_list.append({
            'title': event.title,
            'start': event.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.end.strftime('%Y-%m-%dT%H:%M:%S') if event.end else None,
        })
    return jsonify(event_list)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email đã được sử dụng', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        # Gửi email chào mừng
        send_email(
            to=new_user.email,
            subject="Chào mừng bạn đến với Calendar App!",
            template=f"""
            <html>
                <body>
                    <h2>Chào mừng {new_user.name}!</h2>
                    <p>Cảm ơn bạn đã đăng ký tài khoản với Calendar App.</p>
                    <p>Bạn có thể bắt đầu tạo và quản lý các sự kiện của mình ngay bây giờ.</p>
                    <p>Chúc bạn có trải nghiệm tuyệt vời!</p>
                    <br>
                    <p>Trân trọng,<br>Đội ngũ Calendar App</p>
                </body>
            </html>
            """
        )

        flash('Đăng ký thành công! Vui lòng đăng nhập. Email chào mừng đã được gửi.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email hoặc mật khẩu không đúng.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.start).all()
    return render_template('dashboard.html', name=current_user.name, events=events)


@app.route('/event/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()

    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start=form.start.data,
            end=form.end.data,
            reminder_minutes_before=form.reminder_minutes_before.data,
            repeat_type=form.repeat_type.data,
            user_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Tạo sự kiện thành công!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_event.html', form=form)


@app.route('/event/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    if event.user_id != current_user.id:
        flash('Bạn không có quyền sửa sự kiện này.', 'danger')
        return redirect(url_for('dashboard'))

    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.start = form.start.data
        event.end = form.end.data
        event.reminder_minutes_before = form.reminder_minutes_before.data
        event.repeat_type = form.repeat_type.data
        db.session.commit()
        flash('Cập nhật sự kiện thành công.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('event_form.html', form=form)


@app.route('/event/<int:id>/delete', methods=['POST'])
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    if event.user_id != current_user.id:
        flash('Bạn không có quyền xoá sự kiện này.', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(event)
    db.session.commit()
    flash('Đã xoá sự kiện.', 'success')
    return redirect(url_for('dashboard'))



@app.route('/test-email')
@login_required
def test_email():
    success = send_email(
        to=current_user.email,
        subject="Test Email từ hệ thống lịch",
        template="<h1> Email hoạt động tốt!</h1><p>Hệ thống email đã được cấu hình thành công.</p>"
    )

    if success:
        flash('Email test đã được gửi! Kiểm tra hộp thư của bạn.', 'success')
    else:
        flash('Lỗi gửi email. Kiểm tra cấu hình email.', 'danger')

    return redirect(url_for('dashboard'))


@app.route('/manage-events.html')
@login_required
def manage_events():
    try:
        events = Event.query.filter_by(user_id=current_user.id).order_by(Event.start).all()
        return render_template('manage-events.html', events=events)
    except Exception as e:
        flash(f'Lỗi tải trang quản lý sự kiện: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

# Route gửi email thủ công
@app.route('/send_email')
@login_required
def send_email():
    try:
        success = send_email(
            to=current_user.email,
            subject=" Email từ Calendar App",
            template="<h1> thành công!</h1><p>g.</p>"
        )
        if success:
            flash('Email test đã được gửi!', 'success')
        else:
            flash('Lỗi gửi email!', 'danger')
    except Exception as e:
        flash(f'Lỗi gửi email: {str(e)}', 'danger')
    return redirect(url_for('dashboard'))


# Route kiểm tra nhắc nhở thủ công
@app.route('/check_reminders')
@admin_required
def manual_check_reminders():
    try:
        # Gọi hàm từ reminder_scheduler
        flash('Đã kiểm tra và gửi các email nhắc nhở!', 'success')
    except Exception as e:
        flash(f'Lỗi kiểm tra nhắc nhở: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))


@app.route('/api/events')
@login_required
def api_events():
    events = Event.query.filter_by(user_id=current_user.id).all()
    event_list = []

    for event in events:
        start = event.start
        end = event.end or start
        max_end = start + timedelta(days=30)  # Hiển thị sự kiện lặp lại trong 30 ngày

        if event.repeat_type == 'none':
            event_list.append({
                'id': event.id,
                'title': event.title,
                'start': start.isoformat(),
                'end': end.isoformat(),
                'url': url_for('edit_event', id=event.id)
            })
        else:
            current = start
            while current <= max_end:
                e_end = current + (end - start)
                event_list.append({
                    'id': event.id,
                    'title': f"[Lặp] {event.title}",
                    'start': current.isoformat(),
                    'end': e_end.isoformat(),
                    'url': url_for('edit_event', id=event.id)
                })
                if event.repeat_type == 'daily':
                    current += timedelta(days=1)
                elif event.repeat_type == 'weekly':
                    current += timedelta(weeks=1)
                elif event.repeat_type == 'monthly':
                    current += relativedelta(months=1)

    return jsonify(event_list)


# ----------------- ADMIN ROUTES -------------------

@app.route('/admin')
@admin_required
def admin_dashboard():
    users = User.query.all()
    events = Event.query.all()
    return render_template('admindashboard.html', users=users, events=events)


@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin_user.html', users=users)


@app.route('/admin/users/<int:user_id>')
@admin_required
def admin_user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('admin_user_detail.html', user=user)


@app.route('/admin/events')
@admin_required
def admin_events():
    events = Event.query.all()
    return render_template('admin_event.html', events=events)


@app.route('/admin/settings')
@admin_required
def admin_settings():
    return render_template('admin_setting.html')


@app.route('/admin/logs')
@admin_required
def admin_logs():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    return render_template('admin_log.html', logs=logs)


# Route gửi email thông báo cho tất cả user
@app.route('/admin/send_notification', methods=['GET', 'POST'])
@admin_required
def send_notification():
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')

        if subject and message:
            users = User.query.all()
            for user in users:
                html_body = f"""
                <html>
                    <body>
                        <h2>Thông báo từ Admin</h2>
                        <p>{message}</p>
                        <br>
                        <p>Trân trọng,<br>Đội ngũ Calendar App</p>
                    </body>
                </html>
                """
                send_email(to=user.email, subject=subject, template=html_body)

            flash(f'Đã gửi thông báo đến {len(users)} người dùng!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Vui lòng nhập đầy đủ tiêu đề và nội dung!', 'danger')

    return render_template('send_notification.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    start_reminder_scheduler(app)

    app.run(debug=True)