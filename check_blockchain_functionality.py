from app import create_app, db
from app.models import Airdrop, TokenSale, DaoProposal

app = create_app()
with app.app_context():
    # Проверяем аирдропы
    airdrops = Airdrop.query.all()
    print(f"Аирдропы: найдено {len(airdrops)}")
    for airdrop in airdrops:
        print(f"  ID: {airdrop.id}, Название: {airdrop.title}, Активен: {airdrop.is_active}")
    
    # Проверяем токенсейлы
    tokensales = TokenSale.query.all()
    print(f"\nТокенсейлы: найдено {len(tokensales)}")
    for tokensale in tokensales:
        print(f"  ID: {tokensale.id}, Название: {tokensale.title}, Активен: {tokensale.is_active}")
    
    # Проверяем DAO-предложения
    dao_proposals = DaoProposal.query.all()
    print(f"\nDAO-предложения: найдено {len(dao_proposals)}")
    for proposal in dao_proposals:
        print(f"  ID: {proposal.id}, Название: {proposal.title}, Статус: {proposal.status}")
