# app/admin/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from app.models import db, User, Block, PaymentMethod, Payment, Settings
from app.forms import LoginForm, BlockForm, PaymentMethodForm, SettingsForm

admin = Blueprint('admin', __name__)

def admin_required(func):
    """Декоратор: лише для залогінених адмінів"""
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return wrapper

@admin.route('/login', methods=['GET', 'POST'])
def login():
    """Сторінка логіну в адмінку"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password_hash == form.password.data:  # Для продакшн - хешуйте пароль!
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Невірний логін або пароль', 'danger')
    return render_template('login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    """Вихід з адмінки"""
    logout_user()
    return redirect(url_for('main.index'))

@admin.route('/')
@admin_required
def dashboard():
    """Головна сторінка адмінки"""
    blocks = Block.query.order_by(Block.order).all()
    payments = Payment.query.order_by(Payment.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', blocks=blocks, payments=payments)

@admin.route('/blocks')
@admin_required
def blocks():
    """Список блоків"""
    blocks = Block.query.order_by(Block.order).all()
    return render_template('admin/edit_block.html', blocks=blocks)

@admin.route('/block/edit/<int:block_id>', methods=['GET', 'POST'])
@admin_required
def edit_block(block_id):
    import os
    from werkzeug.utils import secure_filename
    block = Block.query.get_or_404(block_id)
    form = BlockForm(obj=block)
    if form.validate_on_submit():
        form.populate_obj(block)
        # Обробка зображення
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            file = form.image.data
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            block.image = filename
        elif form.image.data and hasattr(form.image.data, 'filename') and not form.image.data.filename:
            # Якщо файл не вибрано, не змінювати поле image
            pass
        db.session.commit()
        flash('Блок збережено', 'success')
        return redirect(url_for('admin.blocks'))
    return render_template('admin/edit_block.html', form=form, block=block)

@admin.route('/payment-methods')
@admin_required
def payment_methods():
    """Список способів оплати"""
    methods = PaymentMethod.query.order_by(PaymentMethod.order).all()
    return render_template('admin/payment_methods.html', methods=methods)

@admin.route('/payment-method/add', methods=['GET', 'POST'])
@admin_required
def add_payment_method():
    """Додавання нового способу оплати"""
    import os
    from werkzeug.utils import secure_filename
    form = PaymentMethodForm()
    if form.validate_on_submit():
        method = PaymentMethod()
        form.populate_obj(method)
        # Обробка файлу QR-коду
        if form.qr_code.data and hasattr(form.qr_code.data, 'filename') and form.qr_code.data.filename:
            file = form.qr_code.data
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            method.qr_code = filename
        elif form.qr_code.data and hasattr(form.qr_code.data, 'filename') and not form.qr_code.data.filename:
            # Якщо файл не вибрано, не змінювати поле qr_code
            pass
        db.session.add(method)
        db.session.commit()
        flash('Метод оплати додано', 'success')
        return redirect(url_for('admin.payment_methods'))
    return render_template('admin/payment_methods.html', form=form)

@admin.route('/payment-method/delete/<int:method_id>', methods=['POST'])
@admin_required
def delete_payment_method(method_id):
    method = PaymentMethod.query.get_or_404(method_id)
    db.session.delete(method)
    db.session.commit()
    flash('Метод оплати видалено', 'success')
    return redirect(url_for('admin.payment_methods'))

@admin.route('/payments')
@admin_required
def payments():
    """Історія оплат"""
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template('admin/payments.html', payments=payments)

@admin.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    """Налаштування сайту"""
    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()
    form = SettingsForm(obj=settings)
    if form.validate_on_submit():
        form.populate_obj(settings)
        db.session.commit()
        flash('Налаштування збережено', 'success')
        return redirect(url_for('admin.settings'))
    return render_template('admin/settings.html', form=form, settings=settings)
