# app/blockchain/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, g, abort
from app.models import Token, Airdrop, AirdropParticipation, TokenSale, TokenPurchase
from app.models import DaoProposal, DaoVote, User
from app.forms import DaoProposalForm
from app import db
from flask_login import current_user, login_required
import json
from datetime import datetime, timedelta

blockchain = Blueprint('blockchain', __name__)

# Маршруты для работы с токеном

@blockchain.route('/token')
def token_info():
    """Информация о токене проекта"""
    token = Token.query.first()
    return render_template('blockchain/token.html', token=token)

# Маршруты для аирдропа

@blockchain.route('/airdrop')
def airdrop_list():
    """Список активных аирдропов"""
    airdrops = Airdrop.query.filter_by(is_active=True).all()
    token = Token.query.first()
    return render_template('blockchain/airdrop_list.html', airdrops=airdrops, token=token)

@blockchain.route('/airdrop/<int:airdrop_id>')
def airdrop_detail(airdrop_id):
    """Детальная страница аирдропа"""
    airdrop = Airdrop.query.get_or_404(airdrop_id)
    token = Token.query.first()
    
    user_participated = False
    if current_user.is_authenticated and current_user.wallet_address:
        # Проверяем, участвовал ли пользователь в аирдропе
        participation = AirdropParticipation.query.filter_by(
            airdrop_id=airdrop_id,
            user_id=current_user.id
        ).first()
        if participation:
            user_participated = True
    
    return render_template('blockchain/airdrop_detail.html', airdrop=airdrop, user_participated=user_participated, token=token)

@blockchain.route('/airdrop/<int:airdrop_id>/participate', methods=['POST'])
def airdrop_participate(airdrop_id):
    """Регистрация на участие в аирдропе"""
    airdrop = Airdrop.query.get_or_404(airdrop_id)
    
    if not airdrop.is_active:
        flash('Этот аирдроп больше не активен.')
        return redirect(url_for('blockchain.airdrop_list'))
    
    wallet_address = request.form.get('wallet_address')
    
    # Проверяем, что адрес кошелька указан и имеет правильный формат
    if not wallet_address or not wallet_address.startswith('0x') or len(wallet_address) != 42:
        flash('Пожалуйста, укажите корректный адрес кошелька Ethereum.')
        return redirect(url_for('blockchain.airdrop_detail', airdrop_id=airdrop_id))
    
    # Проверяем, не участвовал ли этот кошелек или пользователь уже
    existing_participation = AirdropParticipation.query.filter_by(
        airdrop_id=airdrop_id,
        wallet_address=wallet_address
    ).first()
    
    if current_user.is_authenticated:
        existing_user_participation = AirdropParticipation.query.filter_by(
            airdrop_id=airdrop_id,
            user_id=current_user.id
        ).first()
    else:
        existing_user_participation = None
    
    if existing_participation or existing_user_participation:
        flash('Вы уже зарегистрировались на этот аирдроп.')
        return redirect(url_for('blockchain.airdrop_detail', airdrop_id=airdrop_id))
    
    # Создаем запись об участии
    participation = AirdropParticipation(
        airdrop_id=airdrop_id,
        wallet_address=wallet_address,
        amount=airdrop.amount_per_user,
        status='pending'
    )
    
    if current_user.is_authenticated:
        participation.user_id = current_user.id
        
        # Обновляем адрес кошелька пользователя, если его еще нет
        if not current_user.wallet_address:
            user = User.query.get(current_user.id)
            user.wallet_address = wallet_address
    
    db.session.add(participation)
    db.session.commit()
    
    flash('Вы успешно зарегистрировались для участия в аирдропе!')
    return redirect(url_for('blockchain.airdrop_detail', airdrop_id=airdrop_id))

# Маршруты для токенсейла

@blockchain.route('/token-sale')
def token_sale_list():
    """Список токенсейлов"""
    token_sales = TokenSale.query.filter_by(is_active=True).all()
    token = Token.query.first()
    return render_template('blockchain/token_sale_list.html', token_sales=token_sales, token=token)

@blockchain.route('/token-sale/<int:token_sale_id>')
def token_sale_detail(token_sale_id):
    """Детальная страница токенсейла"""
    token_sale = TokenSale.query.get_or_404(token_sale_id)
    token = Token.query.first()  # Информация о токене
    
    user_purchases = []
    if current_user.is_authenticated:
        # Получаем покупки пользователя
        user_purchases = TokenPurchase.query.filter_by(
            token_sale_id=token_sale_id,
            user_id=current_user.id
        ).all()
    
    return render_template('blockchain/token_sale_detail.html', 
                          token_sale=token_sale, 
                          token=token, 
                          user_purchases=user_purchases)

@blockchain.route('/token-sale/<int:token_sale_id>/purchase', methods=['GET', 'POST'])
def token_purchase(token_sale_id):
    """Страница покупки токенов"""
    token_sale = TokenSale.query.get_or_404(token_sale_id)
    token = Token.query.first()
    
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        wallet_address = request.form.get('wallet_address')
        payment_method_id = request.form.get('payment_method_id')
        
        # Валидация данных
        if amount < token_sale.min_purchase or amount > token_sale.max_purchase:
            flash(f'Сумма покупки должна быть от {token_sale.min_purchase} до {token_sale.max_purchase} токенов.')
            return redirect(url_for('blockchain.token_purchase', token_sale_id=token_sale_id))
        
        if not wallet_address or not wallet_address.startswith('0x') or len(wallet_address) != 42:
            flash('Пожалуйста, укажите корректный адрес кошелька Ethereum.')
            return redirect(url_for('blockchain.token_purchase', token_sale_id=token_sale_id))
        
        # Создаем запись о покупке
        purchase = TokenPurchase(
            token_sale_id=token_sale_id,
            wallet_address=wallet_address,
            amount=amount,
            price=token_sale.price,
            total_paid=amount * token_sale.price,
            payment_method_id=payment_method_id,
            status='pending'
        )
        
        if current_user.is_authenticated:
            purchase.user_id = current_user.id
            
            # Обновляем адрес кошелька пользователя, если его еще нет
            if not current_user.wallet_address:
                user = User.query.get(current_user.id)
                user.wallet_address = wallet_address
        
        db.session.add(purchase)
        db.session.commit()
        
        flash('Ваша заявка на покупку токенов принята! Следуйте инструкциям по оплате.')
        return redirect(url_for('blockchain.token_purchase_confirmation', purchase_id=purchase.id))
    
    # Страница формы покупки
    return render_template('blockchain/token_purchase.html', token_sale=token_sale, token=token)

@blockchain.route('/token-purchase/<int:purchase_id>/confirmation')
def token_purchase_confirmation(purchase_id):
    """Страница подтверждения заявки на покупку токенов"""
    purchase = TokenPurchase.query.get_or_404(purchase_id)
    
    # Проверка доступа
    if current_user.is_authenticated and purchase.user_id:
        if purchase.user_id != current_user.id:
            abort(403)
    
    token_sale = TokenSale.query.get(purchase.token_sale_id)
    payment_method = purchase.payment_method
    
    return render_template('blockchain/token_purchase_confirmation.html', 
                          purchase=purchase, 
                          token_sale=token_sale,
                          payment_method=payment_method)

# Маршруты для DAO

@blockchain.route('/dao')
def dao_index():
    """Страница DAO с активными предложениями"""
    active_proposals = DaoProposal.query.filter_by(status='active').all()
    pending_proposals = DaoProposal.query.filter_by(status='pending').all()
    completed_proposals = DaoProposal.query.filter_by(status='completed').all()
    token = Token.query.first()
    
    return render_template('blockchain/dao_index.html', 
                          active_proposals=active_proposals, 
                          pending_proposals=pending_proposals,
                          completed_proposals=completed_proposals,
                          token=token)

@blockchain.route('/dao/proposal/<int:proposal_id>')
def dao_proposal_detail(proposal_id):
    """Детальная страница предложения DAO"""
    proposal = DaoProposal.query.get_or_404(proposal_id)
    token = Token.query.first()
    
    # Проверяем, голосовал ли уже пользователь
    user_voted = False
    user_vote = None
    if current_user.is_authenticated:
        vote = DaoVote.query.filter_by(proposal_id=proposal_id, user_id=current_user.id).first()
        if vote:
            user_voted = True
            user_vote = vote
    
    return render_template('blockchain/dao_proposal_detail.html', 
                          proposal=proposal, 
                          user_voted=user_voted, 
                          user_vote=user_vote,
                          token=token)

@blockchain.route('/dao/proposal/new', methods=['GET', 'POST'])
@login_required
def dao_proposal_new():
    """Создание нового предложения"""
    form = DaoProposalForm()
    
    if form.validate_on_submit():
        # Рассчитываем даты начала и окончания
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=form.duration_days.data)
        
        # Создаём новое предложение
        proposal = DaoProposal(
            title=form.title.data,
            description=form.description.data,
            author_id=current_user.id,
            start_date=start_date,
            end_date=end_date,
            min_tokens_to_vote=form.min_tokens_to_vote.data,
            status='pending'  # Ожидает модерации или автоматического начала
        )
        
        # Копируем заголовок в поля переводов
        proposal.title_ua = form.title.data
        proposal.title_en = form.title.data
        proposal.title_de = form.title.data
        proposal.title_ru = form.title.data
        
        # Копируем описание в поля переводов
        proposal.description_ua = form.description.data
        proposal.description_en = form.description.data
        proposal.description_de = form.description.data
        proposal.description_ru = form.description.data
        
        db.session.add(proposal)
        db.session.commit()
        
        flash('Ваше предложение успешно создано и отправлено на модерацию!')
        return redirect(url_for('blockchain.dao_index'))
    
    return render_template('blockchain/dao_proposal_new.html', form=form)

@blockchain.route('/dao/proposal/<int:proposal_id>/vote', methods=['POST'])
@login_required
def dao_proposal_vote(proposal_id):
    """Голосование за предложение в DAO"""
    proposal = DaoProposal.query.get_or_404(proposal_id)
    
    # Проверяем статус предложения
    if proposal.status != 'active':
        flash('Голосование за это предложение недоступно!')
        return redirect(url_for('blockchain.dao_proposal_detail', proposal_id=proposal_id))
    
    # Проверяем, голосовал ли уже пользователь
    existing_vote = DaoVote.query.filter_by(proposal_id=proposal_id, user_id=current_user.id).first()
    if existing_vote:
        flash('Вы уже голосовали за это предложение!')
        return redirect(url_for('blockchain.dao_proposal_detail', proposal_id=proposal_id))
    
    # Проверяем баланс токенов пользователя
    if current_user.token_balance < proposal.min_tokens_to_vote:
        flash(f'Для голосования необходимо иметь как минимум {proposal.min_tokens_to_vote} токенов!')
        return redirect(url_for('blockchain.dao_proposal_detail', proposal_id=proposal_id))
    
    vote_type = request.form.get('vote_type')
    vote_for = (vote_type == 'for')
    
    # Создаем запись о голосовании
    vote = DaoVote(
        proposal_id=proposal_id,
        user_id=current_user.id,
        wallet_address=current_user.wallet_address,
        vote_weight=current_user.token_balance,  # Вес голоса равен балансу токенов
        vote_for=vote_for
    )
    
    db.session.add(vote)
    
    # Обновляем данные предложения
    if vote_for:
        proposal.votes_for += 1
    else:
        proposal.votes_against += 1
    
    db.session.commit()
    
    flash('Ваш голос учтен!')
    return redirect(url_for('blockchain.dao_proposal_detail', proposal_id=proposal_id))

# API для интеграции с блокчейном
@blockchain.route('/api/token/balance/<wallet_address>')
def token_balance(wallet_address):
    """API для получения баланса токенов по адресу кошелька"""
    # Здесь должен быть вызов к блокчейну или к индексеру для получения баланса
    # Пока возвращаем заглушку
    return jsonify({'balance': 0})

@blockchain.route('/api/token/transfer/confirm', methods=['POST'])
def token_transfer_confirm():
    """API для подтверждения транзакции перевода токенов"""
    data = request.json
    tx_hash = data.get('tx_hash')
    type = data.get('type')  # purchase, vote, shop
    
    if type == 'purchase':
        purchase_id = data.get('purchase_id')
        purchase = TokenPurchase.query.get_or_404(purchase_id)
        purchase.tx_hash = tx_hash
        purchase.status = 'confirmed'
        db.session.commit()
    elif type == 'vote':
        vote_id = data.get('vote_id')
        vote = DaoVote.query.get_or_404(vote_id)
        vote.tx_hash = tx_hash
        db.session.commit()
    
    return jsonify({'success': True})
