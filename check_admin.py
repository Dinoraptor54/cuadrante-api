from models.database import SessionLocal
from models.sql_models import User

db = SessionLocal()
user = db.query(User).filter(User.email == "admin@example.com").first()

if user:
    print(f"User found: {user.email}")
    print(f"Role: {user.role}")
    print(f"Password hash length: {len(user.hashed_password)}")
else:
    print("User NOT found")

db.close()
