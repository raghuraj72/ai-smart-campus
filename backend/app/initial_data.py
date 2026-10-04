import asyncio

from sqlmodel import select

from app.core.database import get_session
from app.core.security import get_password_hash
from app.models.domain import User, UserRole


INITIAL_USERS = [
    {
        "email": "admin@campus.edu",
        "password": "admin123",
        "full_name": "System Administrator",
        "role": UserRole.ADMIN,
        "uid": "ADMIN001",
        "university_code": "CAMPUS",
        "department": "Administration",
    },
    {
        "email": "student@campus.edu",
        "password": "student123",
        "full_name": "Jane Doe",
        "role": UserRole.STUDENT,
        "uid": "STU001",
        "university_code": "CAMPUS",
        "department": "Computer Science",
    },
    {
        "email": "faculty@campus.edu",
        "password": "faculty123",
        "full_name": "Dr. Campus Faculty",
        "role": UserRole.FACULTY,
        "uid": "FAC001",
        "university_code": "CAMPUS",
        "department": "Computer Science",
    },
]


async def init_db():
    async for session in get_session():

        for user_data in INITIAL_USERS:

            result = await session.execute(
                select(User).where(
                    User.email == user_data["email"]
                )
            )

            existing_user = result.scalars().first()

            if existing_user:
                print(
                    f"--> User already exists: "
                    f"{user_data['email']}"
                )
                continue

            user = User(
                email=user_data["email"],
                hashed_password=get_password_hash(
                    user_data["password"]
                ),
                full_name=user_data["full_name"],
                role=user_data["role"],
                uid=user_data["uid"],
                university_code=user_data["university_code"],
                department=user_data["department"],
                is_active=True,
            )

            session.add(user)

            print(
                f"--> Created {user_data['role'].value}: "
                f"{user_data['email']}"
            )

        await session.commit()

        print()
        print("Database initialization complete.")
        break


if __name__ == "__main__":
    asyncio.run(init_db())