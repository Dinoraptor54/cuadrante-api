from models.database import SessionLocal
from models.sql_models import User
from services.auth_service import verify_password, get_password_hash

db = SessionLocal()
email = "user1@cuadrante.com"
user = db.query(User).filter(User.email == email).first()

if user:
    print(f"User found: {user.email}")
    is_valid = verify_password("1234", user.hashed_password)
    print(f"Is '1234' valid? {is_valid}")
    
    if not is_valid:
        print("Resetting password to '1234'...")
        user.hashed_password = get_password_hash("1234")
        db.commit()
        print("Password reset.")
else:
    print(f"User {email} NOT found.")
    # List all users
    users = db.query(User).all()
    print("Available users:")
    for u in users:
        print(f"- {u.email}")

db.close()
