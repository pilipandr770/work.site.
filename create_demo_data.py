from app import create_app, db
from app.utils.demo_data import create_demo_data

app = create_app()

with app.app_context():
    create_demo_data()

print("Демоданные успешно созданы!")
