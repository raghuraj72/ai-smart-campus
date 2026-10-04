from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.deps import get_current_user
from app.core.database import get_session
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.domain import User, UserRole
from app.schemas.auth import (
    LoginRequest,
    Token,
    UserCreate,
    UserRead,
)

router = APIRouter()


@router.post(
    "/signup",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Public student registration endpoint.
    """

    email = user_in.email.lower().strip()

    # Check email
    result = await session.execute(
        select(User).where(User.email == email)
    )

    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Check UID if provided
    if user_in.uid:
        result = await session.execute(
            select(User).where(User.uid == user_in.uid)
        )

        existing_uid = result.scalars().first()

        if existing_uid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="University ID already registered",
            )

    # Public registration always creates STUDENT
    db_user = User(
        email=email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name.strip(),
        role=UserRole.STUDENT,
        uid=user_in.uid,
        university_code=user_in.university_code,
        department=user_in.department,
        is_active=True,
    )

    session.add(db_user)

    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate a user using JSON and return a JWT.
    """

    email = login_data.email.lower().strip()

    result = await session.execute(
        select(User).where(User.email == email)
    )

    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(
        login_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    role_value = (
        user.role.value
        if hasattr(user.role, "value")
        else str(user.role)
    )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": role_value,
        }
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.post(
    "/token",
    response_model=Token,
    include_in_schema=False,
)
async def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """
    OAuth2-compatible login endpoint used by Swagger UI.
    """

    email = form_data.username.lower().strip()

    result = await session.execute(
        select(User).where(User.email == email)
    )

    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    role_value = (
        user.role.value
        if hasattr(user.role, "value")
        else str(user.role)
    )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": role_value,
        }
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserRead,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """

    return current_user

