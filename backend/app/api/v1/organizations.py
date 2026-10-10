from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_session
from app.models.domain import University, Campus, Department


router = APIRouter()


# =========================
# Request / Response Schemas
# =========================

class UniversityCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    code: str = Field(min_length=2, max_length=50)
    country: str = Field(default="India", max_length=100)
    state: str = Field(min_length=2, max_length=100)
    city: str = Field(min_length=2, max_length=100)


class UniversityResponse(BaseModel):
    id: int
    name: str
    code: str
    country: str
    state: str
    city: str
    is_active: bool


class CampusCreate(BaseModel):
    university_id: int
    name: str = Field(min_length=2, max_length=200)
    code: str = Field(min_length=2, max_length=50)
    city: str = Field(min_length=2, max_length=100)


class CampusResponse(BaseModel):
    id: int
    university_id: int
    name: str
    code: str
    city: str
    is_active: bool


class DepartmentCreate(BaseModel):
    campus_id: int
    name: str = Field(min_length=2, max_length=200)
    code: str = Field(min_length=2, max_length=50)


class DepartmentResponse(BaseModel):
    id: int
    campus_id: int
    name: str
    code: str
    is_active: bool


# =========================
# Universities
# =========================

@router.post(
    "/universities",
    response_model=UniversityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_university(
    payload: UniversityCreate,
    session: AsyncSession = Depends(get_session),
):
    existing = await session.execute(
        select(University).where(University.code == payload.code)
    )

    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="University code already exists",
        )

    university = University(**payload.model_dump())

    session.add(university)
    await session.commit()
    await session.refresh(university)

    return university


@router.get(
    "/universities",
    response_model=List[UniversityResponse],
)
async def list_universities(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(University)
        .where(University.is_active == True)
        .order_by(University.name)
    )

    return result.scalars().all()


# =========================
# Campuses
# =========================

@router.post(
    "/campuses",
    response_model=CampusResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_campus(
    payload: CampusCreate,
    session: AsyncSession = Depends(get_session),
):
    university = await session.get(University, payload.university_id)

    if not university:
        raise HTTPException(
            status_code=404,
            detail="University not found",
        )

    campus = Campus(**payload.model_dump())

    session.add(campus)
    await session.commit()
    await session.refresh(campus)

    return campus


@router.get(
    "/campuses",
    response_model=List[CampusResponse],
)
async def list_campuses(
    university_id: int | None = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Campus).where(Campus.is_active == True)

    if university_id is not None:
        query = query.where(Campus.university_id == university_id)

    query = query.order_by(Campus.name)

    result = await session.execute(query)

    return result.scalars().all()


# =========================
# Departments
# =========================

@router.post(
    "/departments",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    payload: DepartmentCreate,
    session: AsyncSession = Depends(get_session),
):
    campus = await session.get(Campus, payload.campus_id)

    if not campus:
        raise HTTPException(
            status_code=404,
            detail="Campus not found",
        )

    department = Department(**payload.model_dump())

    session.add(department)
    await session.commit()
    await session.refresh(department)

    return department


@router.get(
    "/departments",
    response_model=List[DepartmentResponse],
)
async def list_departments(
    campus_id: int | None = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Department).where(Department.is_active == True)

    if campus_id is not None:
        query = query.where(Department.campus_id == campus_id)

    query = query.order_by(Department.name)

    result = await session.execute(query)

    return result.scalars().all()
