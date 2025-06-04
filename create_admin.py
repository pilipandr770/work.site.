from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='andrii770').first():
        # Правильно хешируем пароль перед сохранением
        hashed_password = generate_password_hash('Dnepr 75ok10')
        user = User(username='andrii770', password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        print('Администратор успешно создан!')
    else:
        print('Администратор уже существует!')
