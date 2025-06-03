# app/admin/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from app.models import db, User, Block, PaymentMethod, Payment, Settings, Product, Category, ProductImage
from app.forms import (LoginForm, BlockForm, PaymentMethodForm, SettingsForm, 
                      ProductForm, ProductImageForm, CategoryForm)
from werkzeug.security import check_password_hash
import os
import uuid

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
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Успішно увійшли в систему!', 'success')
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
    from werkzeug.utils import secure_filename
    block = Block.query.get_or_404(block_id)
    form = BlockForm(obj=block)
    if form.validate_on_submit():
        # Явно зберігаємо всі мовні поля
        block.title = form.title.data
        block.title_ua = form.title.data
        block.title_en = form.title_en.data
        block.title_de = form.title_de.data
        block.title_ru = form.title_ru.data
        block.content = form.content.data
        block.content_ua = form.content.data
        block.content_en = form.content_en.data
        block.content_de = form.content_de.data
        block.content_ru = form.content_ru.data
        block.is_active = form.is_active.data
        block.is_top = form.is_top.data
        # Обробка зображення
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            file = form.image.data
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            block.image = filename
        elif form.image.data and hasattr(form.image.data, 'filename') and not form.image.data.filename:
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
    form = PaymentMethodForm()
    return render_template('admin/payment_methods.html', methods=methods, form=form)

@admin.route('/payment-method/add', methods=['GET', 'POST'])
@admin_required
def add_payment_method():
    """Додавання нового способу оплати"""
    from werkzeug.utils import secure_filename
    form = PaymentMethodForm()
    if form.validate_on_submit():
        method = PaymentMethod()
        # Явно зберігаємо всі мовні поля
        method.name = form.name.data
        method.name_ua = form.name.data
        method.name_en = form.name_en.data
        method.name_de = form.name_de.data
        method.name_ru = form.name_ru.data
        method.type = form.type.data
        # details: парсимо JSON якщо можливо
        import json
        try:
            method.details = json.loads(form.details.data) if form.details.data else None
        except Exception:
            method.details = form.details.data
        method.is_active = form.is_active.data
        # Опис
        method.description_ua = form.description_ua.data
        method.description_en = form.description_en.data
        method.description_de = form.description_de.data
        method.description_ru = form.description_ru.data
        # Обробка файлу QR-коду
        if form.qr_code.data and hasattr(form.qr_code.data, 'filename') and form.qr_code.data.filename:
            file = form.qr_code.data
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            method.qr_code = filename
        elif form.qr_code.data and hasattr(form.qr_code.data, 'filename') and not form.qr_code.data.filename:
            pass
        db.session.add(method)
        db.session.commit()
        flash('Метод оплати додано', 'success')
        return redirect(url_for('admin.payment_methods'))
    methods = PaymentMethod.query.order_by(PaymentMethod.order).all()
    return render_template('admin/payment_methods.html', form=form, methods=methods)

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

# ===== УПРАВЛЕНИЕ ПРОДУКТАМИ =====

@admin.route('/products')
@admin_required
def products():
    """Список всех продуктов"""
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=products)

@admin.route('/product/new', methods=['GET', 'POST'])
@admin_required
def product_new():
    """Создание нового продукта"""
    form = ProductForm()
    categories = Category.query.filter_by(is_active=True).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    if form.validate_on_submit():
        product = Product()
        # Явно зберігаємо всі мовні поля та інші поля
        product.name = form.name.data
        product.name_ua = form.name.data
        product.name_en = form.name_en.data
        product.name_de = form.name_de.data
        product.name_ru = form.name_ru.data
        product.slug = form.slug.data
        product.description = form.description.data
        product.description_ua = form.description.data
        product.description_en = form.description_en.data
        product.description_de = form.description_de.data
        product.description_ru = form.description_ru.data
        product.category_id = form.category_id.data
        product.price = form.price.data
        product.token_price = form.token_price.data
        product.example_url = form.example_url.data
        product.delivery_time = form.delivery_time.data
        product.support_period = form.support_period.data
        product.is_digital = form.is_digital.data
        product.is_active = form.is_active.data
        # Обработка features как список
        if form.features.data:
            features_list = [f.strip() for f in form.features.data.split('\n') if f.strip()]
            product.features = features_list
        else:
            product.features = []
        # Обработка изображения
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            filename = str(uuid.uuid4()) + '.' + form.image.data.filename.rsplit('.', 1)[1].lower()
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            form.image.data.save(os.path.join(upload_folder, filename))
            product.image = filename
        db.session.add(product)
        db.session.commit()
        flash('Продукт создан успешно', 'success')
        return redirect(url_for('admin.product_edit', product_id=product.id))
    return render_template('admin/product_form.html', form=form, title='Новый продукт')

@admin.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def product_edit(product_id):
    """Редактирование продукта"""
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    categories = Category.query.filter_by(is_active=True).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    # Заполнение features для формы
    if product.features:
        form.features.data = '\n'.join(product.features)
    if form.validate_on_submit():
        # Явно зберігаємо всі мовні поля та інші поля
        product.name = form.name.data
        product.name_ua = form.name.data
        product.name_en = form.name_en.data
        product.name_de = form.name_de.data
        product.name_ru = form.name_ru.data
        product.slug = form.slug.data
        product.description = form.description.data
        product.description_ua = form.description.data
        product.description_en = form.description_en.data
        product.description_de = form.description_de.data
        product.description_ru = form.description_ru.data
        product.category_id = form.category_id.data
        product.price = form.price.data
        product.token_price = form.token_price.data
        product.example_url = form.example_url.data
        product.delivery_time = form.delivery_time.data
        product.support_period = form.support_period.data
        product.is_digital = form.is_digital.data
        product.is_active = form.is_active.data
        # Обработка features как список
        if form.features.data:
            features_list = [f.strip() for f in form.features.data.split('\n') if f.strip()]
            product.features = features_list
        else:
            product.features = []
        # Обработка изображения
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            filename = str(uuid.uuid4()) + '.' + form.image.data.filename.rsplit('.', 1)[1].lower()
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            form.image.data.save(os.path.join(upload_folder, filename))
            product.image = filename
        elif not product.image:
            product.image = None
        db.session.commit()
        flash('Продукт обновлен успешно', 'success')
        return redirect(url_for('admin.product_edit', product_id=product.id))
    images = ProductImage.query.filter_by(product_id=product.id).order_by(ProductImage.order).all()
    return render_template('admin/product_form.html', form=form, product=product, images=images, title='Редактировать продукт')

@admin.route('/product/<int:product_id>/delete', methods=['POST'])
@admin_required
def product_delete(product_id):
    """Удаление продукта"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Продукт удален', 'success')
    return redirect(url_for('admin.products'))

@admin.route('/product/<int:product_id>/add-image', methods=['GET', 'POST'])
@admin_required
def product_add_image(product_id):
    """Добавление изображения к продукту"""
    product = Product.query.get_or_404(product_id)
    form = ProductImageForm()
    
    if form.validate_on_submit():
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            filename = str(uuid.uuid4()) + '.' + form.image.data.filename.rsplit('.', 1)[1].lower()
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            form.image.data.save(os.path.join(upload_folder, filename))
            
            # Создание записи изображения
            image = ProductImage(
                product_id=product_id,
                image_path=filename,
                title=form.title.data,
                description=form.description.data,
                is_main=form.is_main.data,
                order=ProductImage.query.filter_by(product_id=product_id).count() + 1
            )
            
            # Якщо изображение помечено как главное, убираем флаг з інших
            if form.is_main.data:
                ProductImage.query.filter_by(product_id=product_id, is_main=True).update({'is_main': False})
            
            db.session.add(image)
            db.session.commit()
            flash('Изображение добавлено', 'success')
            return redirect(url_for('admin.product_edit', product_id=product_id))
    
    return render_template('admin/product_image_form.html', form=form, product=product)

@admin.route('/product-image/<int:image_id>/delete', methods=['POST'])
@admin_required
def product_image_delete(image_id):
    """Удаление изображения продукта"""
    image = ProductImage.query.get_or_404(image_id)
    product_id = image.product_id
    db.session.delete(image)
    db.session.commit()
    flash('Изображение удалено', 'success')
    return redirect(url_for('admin.product_edit', product_id=product_id))

# ===== УПРАВЛЕНИЕ КАТЕГОРИЯМИ =====

@admin.route('/categories')
@admin_required
def categories():
    """Список категорий"""
    categories = Category.query.order_by(Category.order).all()
    return render_template('admin/categories.html', categories=categories)

@admin.route('/category/new', methods=['GET', 'POST'])
@admin_required
def category_new():
    """Создание новой категории"""
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category()
        # Явно зберігаємо всі мовні поля та інші поля
        category.name = form.name.data
        category.name_ua = form.name.data
        category.name_en = form.name_en.data
        category.name_de = form.name_de.data
        category.name_ru = form.name_ru.data
        category.slug = form.slug.data
        category.description = form.description.data
        category.description_ua = form.description.data
        category.description_en = form.description_en.data
        category.description_de = form.description_de.data
        category.description_ru = form.description_ru.data
        category.is_active = form.is_active.data
        category.order = form.order.data
        # Обработка изображения
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            filename = str(uuid.uuid4()) + '.' + form.image.data.filename.rsplit('.', 1)[1].lower()
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            form.image.data.save(os.path.join(upload_folder, filename))
            category.image = filename
        db.session.add(category)
        db.session.commit()
        flash('Категория создана успешно', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', form=form, title='Новая категория')

@admin.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@admin_required
def category_edit(category_id):
    """Редактирование категории"""
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        # Явно зберігаємо всі мовні поля та інші поля
        category.name = form.name.data
        category.name_ua = form.name.data
        category.name_en = form.name_en.data
        category.name_de = form.name_de.data
        category.name_ru = form.name_ru.data
        category.slug = form.slug.data
        category.description = form.description.data
        category.description_ua = form.description.data
        category.description_en = form.description_en.data
        category.description_de = form.description_de.data
        category.description_ru = form.description_ru.data
        category.is_active = form.is_active.data
        category.order = form.order.data
        # Обработка изображения
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            filename = str(uuid.uuid4()) + '.' + form.image.data.filename.rsplit('.', 1)[1].lower()
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            form.image.data.save(os.path.join(upload_folder, filename))
            category.image = filename
        db.session.commit()
        flash('Категория обновлена успешно', 'success')
        return redirect(url_for('admin.categories'))
    products_count = Product.query.filter_by(category_id=category_id).count()
    return render_template('admin/category_form.html', form=form, category=category, products_count=products_count, title='Редактировать категорию')

@admin.route('/category/<int:category_id>/delete', methods=['POST'])
@admin_required
def category_delete(category_id):
    """Удаление категории"""
    category = Category.query.get_or_404(category_id)
    products_count = Product.query.filter_by(category_id=category_id).count()
    
    if products_count > 0:
        flash(f'Невозможно удалить категорию: в ней {products_count} продуктов', 'danger')
        return redirect(url_for('admin.categories'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Категория удалена', 'success')
    return redirect(url_for('admin.categories'))
