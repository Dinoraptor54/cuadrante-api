from services.auth_service import verify_password, get_password_hash
from models.database import SessionLocal
from models.sql_models import User

db = SessionLocal()
user = db.query(User).filter(User.email == "admin@example.com").first()

print(f"User: {user.email}")
print(f"Stored Hash: {user.hashed_password}")

is_valid = verify_password("admin123", user.hashed_password)
print(f"Is 'admin123' valid? {is_valid}")

if not is_valid:
    print("Resetting password...")
    new_hash = get_password_hash("admin123")
    user.hashed_password = new_hash
    db.commit()
    print("Password reset to 'admin123'")

db.close()
