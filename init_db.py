"""
Database initialization script with seed data
Run this script to create initial admin user
"""
from app.core.database import SessionLocal, engine
from app.models.models import Base
from app.crud.crud_super_admin import create_super_admin, get_super_admin_by_email
from app.core.security import get_password_hash


def init_db():
    """Initialize database with seed data"""
    # Create all tables first
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if super admin already exists
        admin_email = "superadmin@hrpayroll.com"
        existing_admin = get_super_admin_by_email(db, email=admin_email)

        if existing_admin:
            print(f"Super admin user {admin_email} already exists. Skipping...")
        else:
            from app.schemas.schemas import SuperAdminCreate
            admin_create = SuperAdminCreate(
                email=admin_email,
                password="superadmin123",
                full_name="SaaS Super Admin"
            )
            create_super_admin(db, super_admin=admin_create)
            print(f"Created super admin user: {admin_email}")
            print(f"Password: superadmin123")
            print(f"Please change this password in production!")

        print("Database initialized successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
