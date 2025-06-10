# app/models.py

from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    """Адміністратор сайту"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    wallet_address = db.Column(db.String(42))  # Ethereum/Polygon кошелек
    is_admin = db.Column(db.Boolean, default=False)
    token_balance = db.Column(db.Float, default=0.0)  # Баланс токенов

class Block(db.Model):
    """Контентний блок (для 6 секцій сайту)"""
    __tablename__ = 'block'  # Explicitly set to Latin to match what db.create_all() creates
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    image = db.Column(db.String(256))
    order = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    slug = db.Column(db.String(64), unique=True)
    is_top = db.Column(db.Boolean, default=False)  # Нове поле: головний блок
    title_ua = db.Column(db.String(128))
    title_en = db.Column(db.String(128))
    title_de = db.Column(db.String(128))
    title_ru = db.Column(db.String(128))
    content_ua = db.Column(db.Text)
    content_en = db.Column(db.Text)
    content_de = db.Column(db.Text)
    content_ru = db.Column(db.Text)

class PaymentMethod(db.Model):
    """Метод оплати (Stripe, PayPal, N26, QR, тощо)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.String(32))
    details = db.Column(db.JSON)
    qr_code = db.Column(db.String(256))
    name_ua = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    name_de = db.Column(db.String(64))
    name_ru = db.Column(db.String(64))
    description_ua = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=1)
    invoice_pdf = db.Column(db.String(256))

class Payment(db.Model):
    """Історія/заявки оплат з сайту"""
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    amount = db.Column(db.Float)
    method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    status = db.Column(db.String(32), default='pending') # pending/paid/failed
    payment_info = db.Column(db.JSON)
    invoice_pdf = db.Column(db.String(256))
    proof_image = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    method = db.relationship('PaymentMethod')

class Settings(db.Model):
    """Налаштування сайту"""
    id = db.Column(db.Integer, primary_key=True)
    facebook = db.Column(db.String(256))
    instagram = db.Column(db.String(256))
    telegram = db.Column(db.String(256))
    email = db.Column(db.String(256))
    # Добавляем новые поля для блокчейн интеграции
    contract_address = db.Column(db.String(42))  # Адрес контракта токена
    token_name = db.Column(db.String(64))        # Название токена
    token_symbol = db.Column(db.String(10))      # Символ токена
    network_rpc = db.Column(db.String(256))      # RPC URL сети Polygon
    network_chain_id = db.Column(db.Integer, default=80001)  # Chain ID (80001 для Polygon Mumbai Testnet)

# Новые модели для магазина и блокчейн-функционала

class Category(db.Model):
    """Категория продуктов или услуг"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text)
    image = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=1)
    name_ua = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    name_de = db.Column(db.String(64))
    name_ru = db.Column(db.String(64))
    description_ua = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    """Продукт или услуга"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    slug = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text)
    image = db.Column(db.String(256))
    price = db.Column(db.Float)
    token_price = db.Column(db.Float)  # Цена в токенах
    is_digital = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name_ua = db.Column(db.String(128))
    name_en = db.Column(db.String(128))
    name_de = db.Column(db.String(128))
    name_ru = db.Column(db.String(128))
    description_ua = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    
    # Дополнительные поля для админ-панели
    example_url = db.Column(db.String(512))  # Ссылка на пример работы
    features = db.Column(db.JSON)  # Список функций/особенностей
    delivery_time = db.Column(db.String(128))  # Время выполнения
    support_period = db.Column(db.String(128))  # Период поддержки
    
    # Связи
    images = db.relationship('ProductImage', backref='product', lazy='dynamic', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Product {self.name}>'

class ProductImage(db.Model):
    """Дополнительные изображения продукта"""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    image_path = db.Column(db.String(256))
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=1)
    is_main = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProductImage {self.id}>'

class Cart(db.Model):
    """Корзина покупок"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    items = db.relationship('CartItem', backref='cart', lazy='dynamic', cascade="all, delete-orphan")
    user = db.relationship('User', backref='carts')
    
    def __repr__(self):
        return f'<Cart {self.id}>'

class CartItem(db.Model):
    """Элемент корзины"""
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product')

class Order(db.Model):
    """Заказ"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(32), default='pending')  # pending, paid, processing, completed, cancelled
    total_price = db.Column(db.Float)
    total_token_price = db.Column(db.Float)  # Цена в токенах
    payment_type = db.Column(db.String(32))  # fiat или token
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=True)
    tx_hash = db.Column(db.String(66), nullable=True)  # Хеш транзакции при оплате токенами
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    user = db.relationship('User', backref='orders')
    payment = db.relationship('Payment')
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    """Элемент заказа"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float)  # Цена на момент покупки
    token_price = db.Column(db.Float)  # Цена в токенах на момент покупки
    product = db.relationship('Product')

class Token(db.Model):
    """Информация о токене проекта"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    symbol = db.Column(db.String(10))
    contract_address = db.Column(db.String(42))
    decimals = db.Column(db.Integer, default=18)
    total_supply = db.Column(db.Float)
    circulating_supply = db.Column(db.Float)
    token_price_usd = db.Column(db.Float)  # Текущая цена в USD
    description = db.Column(db.Text)
    description_ua = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Token {self.symbol}>'

class Airdrop(db.Model):
    """Информация об аирдропе"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    total_amount = db.Column(db.Float)  # Общее количество токенов для аирдропа
    amount_per_user = db.Column(db.Float)  # Количество токенов на одного пользователя
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    title_ua = db.Column(db.String(128))
    title_en = db.Column(db.String(128))
    title_de = db.Column(db.String(128))
    title_ru = db.Column(db.String(128))
    description_ua = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    participations = db.relationship('AirdropParticipation', backref='airdrop', lazy='dynamic')
    
    def __repr__(self):
        return f'<Airdrop {self.title}>'

class AirdropParticipation(db.Model):
    """Участие пользователя в аирдропе"""
    id = db.Column(db.Integer, primary_key=True)
    airdrop_id = db.Column(db.Integer, db.ForeignKey('airdrop.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    wallet_address = db.Column(db.String(42))
    amount = db.Column(db.Float)  # Количество токенов
    status = db.Column(db.String(32), default='pending')  # pending, approved, rejected, sent
    tx_hash = db.Column(db.String(66), nullable=True)  # Хеш транзакции
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='airdrop_participations')
    
    def __repr__(self):
        return f'<AirdropParticipation {self.id}>'

class TokenSale(db.Model):
    """Информация о токенсейле"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    total_amount = db.Column(db.Float)  # Общее количество токенов для продажи
    price = db.Column(db.Float)  # Цена токена в USD
    min_purchase = db.Column(db.Float)  # Минимальное количество для покупки
    max_purchase = db.Column(db.Float)  # Максимальное количество для покупки
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    title_ua = db.Column(db.String(128))
    title_en = db.Column(db.String(128))
    title_de = db.Column(db.String(128))
    title_ru = db.Column(db.String(128))
    description_ua = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    purchases = db.relationship('TokenPurchase', backref='token_sale', lazy='dynamic')
    
    def __repr__(self):
        return f'<TokenSale {self.title}>'

class TokenPurchase(db.Model):
    """Покупка токенов в токенсейле"""
    id = db.Column(db.Integer, primary_key=True)
    token_sale_id = db.Column(db.Integer, db.ForeignKey('token_sale.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    wallet_address = db.Column(db.String(42))
    amount = db.Column(db.Float)  # Количество токенов
    price = db.Column(db.Float)  # Цена на момент покупки
    total_paid = db.Column(db.Float)  # Общая сумма оплаты
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'), nullable=True)
    status = db.Column(db.String(32), default='pending')  # pending, confirmed, completed, failed
    tx_hash = db.Column(db.String(66), nullable=True)  # Хеш транзакции
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.relationship('PaymentMethod')
    user = db.relationship('User', backref='token_purchases')
    
    def __repr__(self):
        return f'<TokenPurchase {self.id}>'

class DaoProposal(db.Model):
    """Предложение для голосования в DAO"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    min_tokens_to_vote = db.Column(db.Float, default=1.0)  # Минимум токенов для голосования
    status = db.Column(db.String(32), default='pending')  # pending, active, completed, cancelled
    votes_for = db.Column(db.Integer, default=0)
    votes_against = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    title_ua = db.Column(db.String(128))
    title_en = db.Column(db.String(128))
    title_de = db.Column(db.String(128))
    title_ru = db.Column(db.String(128))
    description_ua = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_de = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    author = db.relationship('User', backref='proposals')
    votes = db.relationship('DaoVote', backref='proposal', lazy='dynamic')
    
    def __repr__(self):
        return f'<DaoProposal {self.title}>'

class DaoVote(db.Model):
    """Голос в DAO предложении"""
    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('dao_proposal.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    wallet_address = db.Column(db.String(42))
    vote_weight = db.Column(db.Float)  # Вес голоса (зависит от количества токенов)
    vote_for = db.Column(db.Boolean)  # True для "за", False для "против"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tx_hash = db.Column(db.String(66), nullable=True)  # Хеш транзакции
    user = db.relationship('User', backref='votes')
    
    def __repr__(self):
        return f'<DaoVote {self.id}>'

class BlogBlock(db.Model):
    """Simplified blog block model - fixed 12 blocks for blog content"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    featured_image = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    position = db.Column(db.Integer, default=1)  # Position from 1-12
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Multi-language support
    title_ua = db.Column(db.String(255), nullable=True)
    title_en = db.Column(db.String(255), nullable=True)
    title_de = db.Column(db.String(255), nullable=True)
    title_ru = db.Column(db.String(255), nullable=True)
    content_ua = db.Column(db.Text, nullable=True)
    content_en = db.Column(db.Text, nullable=True)
    content_de = db.Column(db.Text, nullable=True)
    content_ru = db.Column(db.Text, nullable=True)
    summary_ua = db.Column(db.Text, nullable=True)
    summary_en = db.Column(db.Text, nullable=True)
    summary_de = db.Column(db.Text, nullable=True)
    summary_ru = db.Column(db.Text, nullable=True)

class ImageStorage(db.Model):
    """
    Stores binary image data as backup in case filesystem images are lost.
    References the original filename used in filesystem.
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    binary_data = db.Column(db.LargeBinary)
    content_type = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def store_image(cls, file, filename):
        """Store image binary data in the database"""
        if not file or not filename:
            return None
            
        # Check if image already exists
        existing = cls.query.filter_by(filename=filename).first()
        if existing:
            # Update existing record
            existing.binary_data = file.read()
            existing.content_type = file.content_type if hasattr(file, 'content_type') else None
            db.session.commit()
            file.seek(0)  # Reset file pointer for further use
            return existing
            
        # Create new record
        file.seek(0)  # Ensure at beginning of file
        image_storage = cls(
            filename=filename,
            binary_data=file.read(),
            content_type=file.content_type if hasattr(file, 'content_type') else None
        )
        file.seek(0)  # Reset file pointer for further use
        
        db.session.add(image_storage)
        db.session.commit()
        return image_storage
