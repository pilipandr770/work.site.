from app import create_app, db
from app.models import Settings

app = create_app()
with app.app_context():
    # Обновляем или создаем настройки сайта
    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        
    # Обновляем поля
    settings.facebook = "https://facebook.com/yourproject"
    settings.instagram = "https://instagram.com/yourproject"
    settings.telegram = "https://t.me/yourproject"
    settings.email = "info@yourproject.com"
    settings.contract_address = "0xAf6087a1A730DAb2CA8d42dca7893c22fDBA683d"
    settings.token_name = "IT TOKEN"
    settings.token_symbol = "ITT"
    settings.network_rpc = "https://polygon-mumbai.infura.io/v3/YOUR_API_KEY"
    settings.network_chain_id = 80001
    
    # Сохраняем
    db.session.add(settings)
    db.session.commit()
    
    print("✅ Настройки сайта успешно обновлены!")
