# app/shop/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, jsonify, g, session, current_app
from app.models import Product, Category, Cart, CartItem, Order, OrderItem, User, Payment, Token
from app import db
from flask_login import current_user, login_required
import json
from datetime import datetime

shop = Blueprint('shop', __name__)

@shop.route('/shop')
def index():
    """Главная страница магазина с категориями"""
    categories = Category.query.filter_by(is_active=True).order_by(Category.order).all()
    featured_products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(6).all()
    token = Token.query.first()
    return render_template('shop/index.html', categories=categories, products=featured_products, token=token)

@shop.route('/shop/category/<slug>')
def category(slug):
    """Страница категории с продуктами"""
    category = Category.query.filter_by(slug=slug, is_active=True).first_or_404()
    products = Product.query.filter_by(category_id=category.id, is_active=True).all()
    token = Token.query.first()
    return render_template('shop/category.html', category=category, products=products, token=token)

@shop.route('/shop/product/<slug>')
def product(slug):
    """Страница продукта"""
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    related_products = Product.query.filter_by(category_id=product.category_id, is_active=True)\
                               .filter(Product.id != product.id).limit(3).all()
    
    # Получаем токен для отображения цены в токенах
    token = Token.query.first()
    token_contract_address = current_app.config.get('TOKEN_CONTRACT_ADDRESS')
    token_receiver_address = current_app.config.get('TOKEN_RECEIVER_ADDRESS')
    
    return render_template('shop/product.html', product=product, related_products=related_products, token=token, token_contract_address=token_contract_address, token_receiver_address=token_receiver_address)

@shop.route('/shop/cart')
def cart():
    """Страница корзины"""
    # Если пользователь авторизован, получаем его корзину, иначе из сессии
    cart_items = []
    total = 0
    token_total = 0
    
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id, is_active=True).first()
        if cart:
            cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            for item in cart_items:
                total += item.product.price * item.quantity
                token_total += item.product.token_price * item.quantity
    else:
        # Для неавторизованных пользователей используем сессию
        session_cart = session.get('cart', {})
        for product_id, quantity in session_cart.items():
            product = Product.query.get(product_id)
            if product:
                cart_items.append({
                    'product': product,
                    'quantity': quantity
                })
                total += product.price * quantity
                token_total += product.token_price * quantity
    
    token = Token.query.first()  # Получаем информацию о токене
    # Додаємо передачу адрес з config
    token_contract_address = current_app.config.get('TOKEN_CONTRACT_ADDRESS')
    token_receiver_address = current_app.config.get('TOKEN_RECEIVER_ADDRESS')
    return render_template('shop/cart.html', cart_items=cart_items, total=total, token_total=token_total, token=token, token_contract_address=token_contract_address, token_receiver_address=token_receiver_address)

@shop.route('/shop/cart/add', methods=['POST'])
def add_to_cart():
    """Добавление товара в корзину"""
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    product = Product.query.get_or_404(product_id)
    
    if current_user.is_authenticated:
        # Для авторизованных пользователей сохраняем в БД
        cart = Cart.query.filter_by(user_id=current_user.id, is_active=True).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if cart_item:
            # Если товар уже в корзине, увеличиваем количество
            cart_item.quantity += quantity
        else:
            # Иначе добавляем новый элемент
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
        
        db.session.commit()
    else:
        # Для неавторизованных пользователей сохраняем в сессии
        cart = session.get('cart', {})
        if product_id in cart:
            cart[product_id] = cart[product_id] + quantity
        else:
            cart[product_id] = quantity
        session['cart'] = cart
    
    flash('Товар успешно добавлен в корзину!')
    return redirect(url_for('shop.product', slug=product.slug))

@shop.route('/shop/checkout', methods=['GET', 'POST'])
def checkout():
    """Страница оформления заказа"""
    if request.method == 'POST':
        # Обработка заказа
        payment_type = request.form.get('payment_type')  # fiat или token
        
        # Создаем заказ
        order = Order(
            user_id=current_user.id if current_user.is_authenticated else None,
            status='pending',
            payment_type=payment_type
        )
        db.session.add(order)
        db.session.flush()
        
        total = 0
        token_total = 0
        
        # Обрабатываем товары из корзины
        if current_user.is_authenticated:
            cart = Cart.query.filter_by(user_id=current_user.id, is_active=True).first()
            if cart:
                cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
                for item in cart_items:
                    product = Product.query.get(item.product_id)
                    if product:
                        order_item = OrderItem(
                            order_id=order.id,
                            product_id=product.id,
                            quantity=item.quantity,
                            price=product.price,
                            token_price=product.token_price
                        )
                        db.session.add(order_item)
                        
                        total += product.price * item.quantity
                        token_total += product.token_price * item.quantity
                
                # Деактивируем корзину после создания заказа
                cart.is_active = False
                db.session.commit()
        else:
            # Для неавторизованных пользователей используем сессию
            session_cart = session.get('cart', {})
            for product_id, quantity in session_cart.items():
                product = Product.query.get(product_id)
                if product:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=quantity,
                        price=product.price,
                        token_price=product.token_price
                    )
                    db.session.add(order_item)
                    
                    total += product.price * quantity
                    token_total += product.token_price * quantity
            
            session.pop('cart', None)  # Очищаем корзину в сессии
        
        # Обновляем общую сумму заказа
        order.total_price = total
        order.total_token_price = token_total
        
        if payment_type == 'fiat':
            # Создаем запись платежа
            payment = Payment(
                user_name=request.form.get('name'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                amount=total,
                method_id=request.form.get('payment_method_id'),
                status='pending'
            )
            db.session.add(payment)
            db.session.flush()
            
            order.payment_id = payment.id
        elif payment_type == 'token':
            # Для оплаты токенами пока просто отмечаем тип платежа,
            # транзакцию пользователь будет выполнять на фронтенде
            pass
        
        db.session.commit()
        
        return redirect(url_for('shop.order_confirmation', order_id=order.id))
    
    # Страница оформления заказа
    token = Token.query.first()  # Получаем информацию о токене
    return render_template('shop/checkout.html', token=token)

@shop.route('/shop/order/<int:order_id>/confirmation')
def order_confirmation(order_id):
    """Страница подтверждения заказа"""
    order = Order.query.get_or_404(order_id)
    
    # Если заказ принадлежит авторизованному пользователю или заказ анонимный
    if (current_user.is_authenticated and order.user_id == current_user.id) or not order.user_id:
        return render_template('shop/order_confirmation.html', order=order)
    else:
        abort(403)

@shop.route('/shop/orders')
@login_required
def orders():
    """Страница с заказами пользователя"""
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('shop/orders.html', orders=user_orders)

@shop.route('/shop/bots')
def bots():
    """Сторінка с Telegram-ботами"""
    bots_category = Category.query.filter(Category.name.ilike('%бот%')).first()
    products = []
    if bots_category:
        products = Product.query.filter_by(category_id=bots_category.id, is_active=True).all()
    token = Token.query.first()
    return render_template('shop/bots.html', products=products, token=token)

@shop.route('/shop/websites')
def websites():
    """Сторінка с веб-сайтами"""
    websites_category = Category.query.filter(Category.name.ilike('%сайт%')).first()
    products = []
    if websites_category:
        products = Product.query.filter_by(category_id=websites_category.id, is_active=True).all()
    token = Token.query.first()
    return render_template('shop/websites.html', products=products, token=token)

# API маршруты для взаимодействия с фронтендом (Ajax)
@shop.route('/api/cart/update', methods=['POST'])
def update_cart():
    """API для обновления количества товаров в корзине"""
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id, is_active=True).first()
        if cart:
            item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
            if item:
                if quantity > 0:
                    item.quantity = quantity
                    db.session.commit()
                else:
                    db.session.delete(item)
                    db.session.commit()
    else:
        cart = session.get('cart', {})
        if product_id in cart:
            if quantity > 0:
                cart[product_id] = quantity
            else:
                del cart[product_id]
            session['cart'] = cart
    
    return jsonify({'success': True})

@shop.route('/api/token/transfer', methods=['POST'])
def token_transfer():
    """API для обновления статуса заказа после оплаты токенами"""
    data = request.json
    order_id = data.get('order_id')
    tx_hash = data.get('tx_hash')
    
    order = Order.query.get_or_404(order_id)
    order.tx_hash = tx_hash
    order.status = 'paid'
    db.session.commit()
    
    return jsonify({'success': True})
