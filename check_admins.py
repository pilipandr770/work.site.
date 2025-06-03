from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    for u in users:
        print(f"username={u.username}, password_hash={u.password_hash}")
