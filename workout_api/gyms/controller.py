from typing import List
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.gyms.schemas import GymIn, GymOut
from workout_api.gyms.models import GymModel

from workout_api.contrib.dependencies import DatabaseDependency


router = APIRouter()

@router.post(
        path = '/',
        summary = "Add new gym",
        status_code = status.HTTP_201_CREATED,
        response_model = GymOut
)

async def post(
    db_session: DatabaseDependency,
    gym_in: GymIn = Body(...)
) -> GymOut:
    
    # Check if Name is already in use
    if ((await db_session.execute(select(GymModel).filter_by(name = gym_in.name))).scalars().first()):
        raise HTTPException(
            status_code = status.HTTP_303_SEE_OTHER,
            detail=f"Gym name: {gym_in.name} already in use"
        )
    
    gym_out = GymOut(id=uuid4(), **gym_in.model_dump())
    gym_model = GymModel(**gym_out.model_dump())
    db_session.add(gym_model)
    await db_session.commit()
    return gym_out


@router.get(
        path = '/',
        summary = "List all Gyms",
        status_code = status.HTTP_200_OK,
        response_model = Page[GymOut]
)

async def query(db_session: DatabaseDependency) -> Page[GymOut]:
    gyms: List[GymOut] = (await db_session.execute(select(GymModel))).scalars().all()
    return paginate(gyms)

@router.get(
        path = '/name:{name}',
        summary = "Find Gym by name",
        status_code = status.HTTP_200_OK,
        response_model = Page[GymOut]
)

async def query(name: str, db_session: DatabaseDependency) -> Page[GymOut]:
    
    query = select(GymModel).where(GymModel.name.contains(name))
    results = await db_session.execute(query)
    gym: List[GymOut] = results.scalars().all()

    
    if not gym:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Gym not found by name: {name}")

    return paginate(gym)

@router.get(
        path = '/{id}',
        summary = "Find Gym by ID",
        status_code = status.HTTP_200_OK,
        response_model = GymOut
)

async def query(id: UUID4, db_session: DatabaseDependency) -> GymOut:
    gym: GymOut = (
        await db_session.execute(select(GymModel).filter_by(id = id))
    ).scalars().first()
    
    if not gym:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Gym not found: {id}")

    return gym