from app import create_app, db
from app.models import Settings, Token

app = create_app()
with app.app_context():
    # Проверяем настройки сайта
    settings = Settings.query.first()
    if settings:
        print("=== Настройки сайта ===")
        print(f"Facebook: {settings.facebook}")
        print(f"Instagram: {settings.instagram}")
        print(f"Telegram: {settings.telegram}")
        print(f"Email: {settings.email}")
        print(f"Contract Address: {settings.contract_address}")
        print(f"Token Name: {settings.token_name}")
        print(f"Token Symbol: {settings.token_symbol}")
        print(f"Network RPC: {settings.network_rpc}")
        print(f"Network Chain ID: {settings.network_chain_id}")
    else:
        print("❌ Настройки сайта не найдены")

    # Проверяем настройки токена
    token = Token.query.first()
    if token:
        print("\n=== Настройки токена ===")
        print(f"Name: {token.name}")
        print(f"Symbol: {token.symbol}")
        print(f"Contract Address: {token.contract_address}")
        print(f"Decimals: {token.decimals}")
        print(f"Total Supply: {token.total_supply}")
        print(f"Circulating Supply: {token.circulating_supply}")
        print(f"Token Price (USD): {token.token_price_usd}")
    else:
        print("❌ Настройки токена не найдены")
