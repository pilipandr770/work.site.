from app import create_app, db
from app.models import User
import sys

app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='andrii770').first()
    if admin:
        print(f"✅ Администратор найден в базе данных!")
        print(f"Имя пользователя: {admin.username}")
        print(f"Хеш пароля: {admin.password_hash[:20]}... (скрыт)")
    else:
        print(f"❌ Администратор 'andrii770' НЕ НАЙДЕН в базе данных!")
        print("Необходимо создать администратора")
        sys.exit(1)
