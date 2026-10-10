import asyncio

from sqlmodel import select

from app.core.database import engine
from app.core.security import get_password_hash
from app.models.domain import User, UserRole
from sqlalchemy.ext.asyncio import AsyncSession


async def create_admin():
    email = "admin@smartcampus.local"
    password = "Admin@12345"

    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(User).where(User.email == email)
        )

        existing_user = result.scalars().first()

        if existing_user:
            print("Admin already exists.")
            print("Email:", email)
            return

        admin = User(
            email=email,
            hashed_password=get_password_hash(password),
            full_name="Smart Campus Admin",
            role=UserRole.ADMIN,
            is_active=True,
        )

        session.add(admin)
        await session.commit()
        await session.refresh(admin)

        print("Admin created successfully.")
        print("ID:", admin.id)
        print("Email:", email)
        print("Password:", password)
        print("Role:", admin.role)


if __name__ == "__main__":
    asyncio.run(create_admin())