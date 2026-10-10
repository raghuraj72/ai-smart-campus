import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import engine
from app.models.domain import User


async def main():
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(User).where(
                User.email == "admin@smartcampus.local"
            )
        )

        user = result.scalars().first()

        if not user:
            print("Admin user not found.")
            return

        user.email = "admin@smartcampus.com"

        session.add(user)
        await session.commit()

        print("Admin email updated successfully.")


asyncio.run(main())