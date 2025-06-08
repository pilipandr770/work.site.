from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Удаляем существующего пользователя
    existing_user = User.query.filter_by(username='andrii770').first()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        print("Старый пользователь удален")
    
    # Создаем нового с правильным хешем
    password_hash = generate_password_hash('Dnepr75ok10')
    print(f"Создается хеш: {password_hash}")
    
    user = User(username='andrii770', password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    print('Новый админ создан!')
    
    # Проверяем сразу
    from werkzeug.security import check_password_hash
    is_valid = check_password_hash(user.password_hash, 'Dnepr75ok10')
    print(f"Проверка пароля: {is_valid}")