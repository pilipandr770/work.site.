# app/main/routes.py

from flask import Blueprint, render_template, redirect, url_for, abort, g, session, current_app
from app.models import Block, PaymentMethod, Settings, Category, Product
from app.models import Token, Airdrop, TokenSale, DaoProposal
from app import db

main = Blueprint('main', __name__)

# Вспомогательные функции для получения локализованного контента
def get_block_title(block):
    """Получает заголовок блока в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.title_ua or block.title
    elif lang == 'en':
        return block.title_en or block.title
    elif lang == 'de':
        return block.title_de or block.title
    elif lang == 'ru':
        return block.title_ru or block.title
    return block.title

def get_block_content(block):
    """Получает содержимое блока в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.content_ua or block.content
    elif lang == 'en':
        return block.content_en or block.content
    elif lang == 'de':
        return block.content_de or block.content
    elif lang == 'ru':
        return block.content_ru or block.content
    return block.content

# Новые вспомогательные функции для многоязычного контента
def get_category_name(category):
    """Получает имя категории в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return category.name_ua or category.name
    elif lang == 'en':
        return category.name_en or category.name
    elif lang == 'de':
        return category.name_de or category.name
    elif lang == 'ru':
        return category.name_ru or category.name
    return category.name

def get_product_name(product):
    """Получает имя продукта в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return product.name_ua or product.name
    elif lang == 'en':
        return product.name_en or product.name
    elif lang == 'de':
        return product.name_de or product.name
    elif lang == 'ru':
        return product.name_ru or product.name
    return product.name

def get_product_description(product):
    """Получает описание продукта в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return product.description_ua or product.description
    elif lang == 'en':
        return product.description_en or product.description
    elif lang == 'de':
        return product.description_de or product.description
    elif lang == 'ru':
        return product.description_ru or product.description
    return product.description

def get_token_description(token):
    """Получает описание токена в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return token.description_ua or token.description
    elif lang == 'en':
        return token.description_en or token.description
    elif lang == 'de':
        return token.description_de or token.description
    elif lang == 'ru':
        return token.description_ru or token.description
    return token.description

def get_airdrop_title(airdrop):
    """Получает заголовок аирдропа в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return airdrop.title_ua or airdrop.title
    elif lang == 'en':
        return airdrop.title_en or airdrop.title
    elif lang == 'de':
        return airdrop.title_de or airdrop.title
    elif lang == 'ru':
        return airdrop.title_ru or airdrop.title
    return airdrop.title

def get_airdrop_description(airdrop):
    """Получает описание аирдропа в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return airdrop.description_ua or airdrop.description
    elif lang == 'en':
        return airdrop.description_en or airdrop.description
    elif lang == 'de':
        return airdrop.description_de or airdrop.description
    elif lang == 'ru':
        return airdrop.description_ru or airdrop.description
    return airdrop.description

def get_token_sale_title(token_sale):
    """Получает заголовок токенсейла в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return token_sale.title_ua or token_sale.title
    elif lang == 'en':
        return token_sale.title_en or token_sale.title
    elif lang == 'de':
        return token_sale.title_de or token_sale.title
    elif lang == 'ru':
        return token_sale.title_ru or token_sale.title
    return token_sale.title

def get_token_sale_description(token_sale):
    """Получает описание токенсейла в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return token_sale.description_ua or token_sale.description
    elif lang == 'en':
        return token_sale.description_en or token_sale.description
    elif lang == 'de':
        return token_sale.description_de or token_sale.description
    elif lang == 'ru':
        return token_sale.description_ru or token_sale.description
    return token_sale.description

def get_dao_proposal_title(proposal):
    """Получает заголовок предложения DAO в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return proposal.title_ua or proposal.title
    elif lang == 'en':
        return proposal.title_en or proposal.title
    elif lang == 'de':
        return proposal.title_de or proposal.title
    elif lang == 'ru':
        return proposal.title_ru or proposal.title
    return proposal.title

def get_dao_proposal_description(proposal):
    """Получает описание предложения DAO в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return proposal.description_ua or proposal.description
    elif lang == 'en':
        return proposal.description_en or proposal.description
    elif lang == 'de':
        return proposal.description_de or proposal.description
    elif lang == 'ru':
        return proposal.description_ru or proposal.description
    return proposal.description

@main.route('/')
def index():
    """Головна сторінка з блоками"""
    blocks = Block.query.filter_by(is_active=True).order_by(Block.order).all()
    methods = PaymentMethod.query.filter_by(is_active=True).order_by(PaymentMethod.order).all()
    settings = Settings.query.first()
    token = Token.query.first()  # Получаем информацию о токене
    bots_category = Category.query.filter(Category.name.ilike('%бот%')).first()
    bots_products = Product.query.filter_by(category_id=bots_category.id, is_active=True).order_by(Product.created_at.desc()).limit(3).all() if bots_category else []
    return render_template('index.html', blocks=blocks, methods=methods, settings=settings, token=token, bots_products=bots_products)

@main.route('/block/<slug>')
def block_detail(slug):
    """Детальна сторінка блоку"""
    block = Block.query.filter_by(slug=slug, is_active=True).first_or_404()
    return render_template('block_detail.html', block=block)

@main.route('/payment')
def payment():
    """Сторінка з усіма методами оплати"""
    methods = PaymentMethod.query.filter_by(is_active=True).order_by(PaymentMethod.order).all()
    token_contract_address = current_app.config.get('TOKEN_CONTRACT_ADDRESS')
    token_receiver_address = current_app.config.get('TOKEN_RECEIVER_ADDRESS')
    return render_template('payment.html', methods=methods, config={
        'TOKEN_CONTRACT_ADDRESS': token_contract_address,
        'TOKEN_RECEIVER_ADDRESS': token_receiver_address
    })

@main.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main.route('/impressum')
def impressum():
    return render_template('impressum.html')

@main.route('/contacts')
def contacts():
    return render_template('contacts.html')
