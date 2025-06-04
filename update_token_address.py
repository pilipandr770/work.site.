from app import create_app, db
from app.models import Settings, Token
import os

app = create_app()
with app.app_context():
    # Получаем реальный адрес токена из переменной окружения
    token_address = os.environ.get('TOKEN_CONTRACT_ADDRESS', '0xAf6087a1A730DAb2CA8d42dca7893c22fDBA683d')
    receiver_address = os.environ.get('TOKEN_RECEIVER_ADDRESS', '0x917544120060Feb4571CdB14dBCC1e4d8005c218')
    
    print(f"Используем адрес контракта токена: {token_address}")
    print(f"Используем адрес получателя токенов: {receiver_address}")
    
    # Обновляем настройки сайта
    settings = Settings.query.first()
    if settings:
        settings.contract_address = token_address
        db.session.commit()
        print("✅ Адрес контракта токена обновлен в настройках сайта")
    else:
        print("❌ Настройки сайта не найдены")
    
    # Обновляем настройки токена
    token = Token.query.first()
    if token:
        token.contract_address = token_address
        db.session.commit()
        print("✅ Адрес контракта токена обновлен в настройках токена")
    else:
        print("❌ Настройки токена не найдены")
    
    print("\nПроверка обновленных настроек:")
    
    if settings:
        print(f"Настройки сайта - Contract Address: {settings.contract_address}")
    
    if token:
        print(f"Настройки токена - Contract Address: {token.contract_address}")
