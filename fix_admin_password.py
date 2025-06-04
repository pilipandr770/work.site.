from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='andrii770').first()
    if user:
        # Исправляем: заменяем текстовый пароль на хеш
        plain_password = user.password_hash  # Текущий пароль в открытом виде
        print(f"Текущий пароль (в открытом виде): {plain_password}")
        
        # Создаем хеш пароля
        hashed_password = generate_password_hash(plain_password)
        print(f"Новый хешированный пароль: {hashed_password[:20]}...")
        
        # Обновляем пароль в базе данных
        user.password_hash = hashed_password
        db.session.commit()
        print("✅ Пароль успешно обновлен! Теперь вы можете войти в систему.")
    else:
        print("❌ Пользователь 'andrii770' не найден!")
