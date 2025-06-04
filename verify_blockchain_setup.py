from app import create_app, db
from app.models import Token, Airdrop, TokenSale, DaoProposal
import os

app = create_app()

def verify_blockchain_setup():
    """Проверяет корректность настройки блокчейн-функционала"""
    print("=" * 60)
    print("ПРОВЕРКА БЛОКЧЕЙН-ФУНКЦИОНАЛА")
    print("=" * 60)
    
    with app.app_context():
        # Получаем реальный адрес токена из переменной окружения
        env_token_address = os.environ.get('TOKEN_CONTRACT_ADDRESS', '0xAf6087a1A730DAb2CA8d42dca7893c22fDBA683d')
        print(f"Адрес токена из переменных окружения: {env_token_address}")
        
        # Проверяем токен в базе данных
        token = Token.query.first()
        if token:
            print(f"\n1. ТОКЕН:")
            print(f"   Имя: {token.name}")
            print(f"   Символ: {token.symbol}")
            print(f"   Адрес контракта: {token.contract_address}")
            
            if token.contract_address == env_token_address:
                print(f"   ✅ Адрес контракта совпадает с переменной окружения")
            else:
                print(f"   ❌ ОШИБКА: Адрес контракта в БД ({token.contract_address}) не совпадает с переменной окружения ({env_token_address})")
        else:
            print(f"\n❌ ОШИБКА: Токен не найден в базе данных")
        
        # Проверяем аирдропы
        airdrops = Airdrop.query.all()
        print(f"\n2. АИРДРОПЫ: {len(airdrops)}")
        for i, airdrop in enumerate(airdrops, 1):
            print(f"   {i}. {airdrop.title}")
            print(f"      Количество на пользователя: {airdrop.amount_per_user}")
            print(f"      Всего токенов: {airdrop.total_amount}")
            print(f"      Активен: {airdrop.is_active}")
        
        # Проверяем токенсейлы
        tokensales = TokenSale.query.all()
        print(f"\n3. ТОКЕНСЕЙЛЫ: {len(tokensales)}")
        for i, tokensale in enumerate(tokensales, 1):
            print(f"   {i}. {tokensale.title}")
            print(f"      Цена: ${tokensale.price}")
            print(f"      Всего токенов: {tokensale.total_amount}")
            print(f"      Активен: {tokensale.is_active}")
        
        # Проверяем DAO предложения
        proposals = DaoProposal.query.all()
        print(f"\n4. DAO ПРЕДЛОЖЕНИЯ: {len(proposals)}")
        for i, proposal in enumerate(proposals, 1):
            print(f"   {i}. {proposal.title}")
            print(f"      Статус: {proposal.status}")
            print(f"      Голоса ЗА: {proposal.votes_for}")
            print(f"      Голоса ПРОТИВ: {proposal.votes_against}")
        
        print("\n" + "=" * 60)
        print("✅ ПРОВЕРКА БЛОКЧЕЙН-ФУНКЦИОНАЛА ЗАВЕРШЕНА")
        print("=" * 60)

if __name__ == "__main__":
    verify_blockchain_setup()
