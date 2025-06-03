from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='andrii770').first():
        user = User(username='andrii770', password_hash='Dnepr 75ok10')
        db.session.add(user)
        db.session.commit()
        print('Адміна створено!')
    else:
        print('Адмін вже існує!')
