from typing import List
from enum import Enum
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from pydantic import UUID4
from uuid import uuid4
from datetime import datetime
from sqlalchemy.future import select
from workout_api.athletes.schemas import AthleteIn, AthleteOut, AthleteUpdate
from workout_api.athletes.models import AthleteModel
import workout_api.athletes.config as athlete_config

from workout_api.categories.models import CategoryModel
from workout_api.categories.schemas import CategoryOut
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.gyms.models import GymModel
from workout_api.gyms.schemas import GymAthlete

from workout_api.helper.input_validator import InputValidator

class Sex(str, Enum):
    male = "m"
    female = "f"



router = APIRouter()

@router.post(
        path = '/',
        summary = "Add new athlete",
        status_code = status.HTTP_201_CREATED,
        response_model = AthleteOut,
)

async def post(
    db_session: DatabaseDependency,
    athlete_in: AthleteIn = Body(...)
) -> AthleteOut:
    
    category_name = athlete_in.category.name
    category: CategoryOut = (await db_session.execute(select(CategoryModel).filter_by(name = category_name))).scalars().first()
    # Check if category exists
    if not category:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Category {category_name} not found."
        )
    # Check if gym exists
    gym_name = athlete_in.gym.name
    gym: GymModel = (await db_session.execute(select(GymModel).filter_by(name = gym_name))).scalars().first()
    if not gym:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Gym {gym_name} not found."
        )
    # Check if CPF is valid
    if not InputValidator.is_valid_cpf(athlete_in.cpf):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=f"CPF {athlete_in.cpf} is not valid"
        )
    # Check if sex is either M or F
    if not InputValidator.is_input_in_list(input = athlete_in.sex.lower(), options = ["m", "f"]):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=f"Sex {athlete_in.sex} is not valid"
        )
    # Save the sex in lower case
    athlete_in.sex = athlete_in.sex.lower()
    
    # Check if weight is within the upper limit
    if athlete_in.weight > athlete_config.max_weight:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=f"Weight {athlete_in.weight} is too high. Max weight is {athlete_config.max_weight}"
        )
    
    # Check if weight is within the upper limit
    if athlete_in.height > athlete_config.max_height:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=f"Height {athlete_in.height} is probably wrong. Max height is {athlete_config.max_height}. Insert height in meters"
        )

    # Check if Name is already in use
    if ((await db_session.execute(select(AthleteModel).filter_by(cpf = athlete_in.cpf))).scalars().first()):
        raise HTTPException(
            status_code = status.HTTP_303_SEE_OTHER,
            detail=f"CPF {athlete_in.cpf} already in use"
        )

    try:
        athlete_out = AthleteOut(id=uuid4(), created_at = datetime.now() ,**athlete_in.model_dump())
        athlete_model = AthleteModel(**athlete_out.model_dump(exclude={"category", "gym"}))
        athlete_model.category_id = category.pk_id
        athlete_model.gym_id = gym.pk_id
        db_session.add(athlete_model)
        await db_session.commit()
    
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inserting data in DB"
        )
    return athlete_out

@router.get(
        path = '/',
        summary = "List all Athletes",
        status_code = status.HTTP_200_OK,
        response_model = Page[AthleteOut]
)

async def get_all_athletes(db_session: DatabaseDependency) -> Page[AthleteOut]:
    athletes: List[AthleteOut] = (await db_session.execute(select(AthleteModel))).scalars().all()
    #print(athletes)
    #print(type(athletes))
    #return ([AthleteOut.model_validate(athlete) for athlete in athletes])
    return paginate(athletes)

@router.get(
        path = '/name:{name}',
        summary = "Find Athlete by name",
        status_code = status.HTTP_200_OK,
        response_model = Page[AthleteOut]
)

async def get_athlete_by_name(name: str, db_session: DatabaseDependency) -> Page[AthleteOut]:
    
    query = select(AthleteModel).where(AthleteModel.name.contains(name))
    results = await db_session.execute(query)
    athlete: List[AthleteOut] = results.scalars().all()

    
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Athlete not found by name: {name}")

    return paginate(athlete)

@router.get(
        path = '/cpf:{cpf}',
        summary = "Find Athlete by CPF",
        status_code = status.HTTP_200_OK,
        response_model = Page[AthleteOut]
)

async def get_athlete_by_cpf(cpf: str, db_session: DatabaseDependency) -> Page[AthleteOut]:
    
    query = select(AthleteModel).where(AthleteModel.cpf.contains(cpf))
    results = await db_session.execute(query)
    athlete: List[AthleteOut] = results.scalars().all()

    
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Athlete not found by CPF: {cpf}")

    return paginate(athlete)

@router.get(
        path = '/sex:{sex}',
        summary = "Find Athlete by Sex",
        status_code = status.HTTP_200_OK,
        response_model = Page[AthleteOut],
            
)

async def get_athlete_by_sex(sex: Sex, db_session: DatabaseDependency) -> Page[AthleteOut]:
    
    query = select(AthleteModel).filter_by(sex = sex)
    results = await db_session.execute(query)
    athlete: List[AthleteOut] = results.scalars().all()

    
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Athlete not found by sex: {sex}")

    return paginate(athlete)


@router.get(
        path = '/age:{age}',
        summary = "Find Athlete by Age",
        status_code = status.HTTP_200_OK,
        response_model = Page[AthleteOut]
)

async def get_athlete_by_age(db_session: DatabaseDependency, min_age: int = 0, max_age: int = 200) -> Page[AthleteOut]:
    
    query = select(AthleteModel).filter(AthleteModel.age >= min_age, AthleteModel.age <= max_age)
    results = await db_session.execute(query)
    athlete: List[AthleteOut] = results.scalars().all()

    
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Athlete not found by age: min {min_age}, max {max_age}")

    return paginate(athlete)

@router.get(
        path = '/weight:{weight}',
        summary = "Find Athlete by Weight",
        status_code = status.HTTP_200_OK,
        response_model = Page[AthleteOut]
)

async def get_athlete_by_weight(db_session: DatabaseDependency, min_weight: int = 0, max_weight: int = athlete_config.max_weight) -> Page[AthleteOut]:
    
    query = select(AthleteModel).filter(AthleteModel.weight >= min_weight, AthleteModel.weight <= max_weight)
    results = await db_session.execute(query)
    athlete: List[AthleteOut] = results.scalars().all()

    
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Athlete not found by weight: min {min_weight}, max {max_weight}")

    return paginate(athlete)

@router.get(
        path = '/height:{height}',
        summary = "Find Athlete by Height",
        status_code = status.HTTP_200_OK,
        response_model = Page[AthleteOut]
)

async def get_athlete_by_height(db_session: DatabaseDependency, min_height: int = 0, max_height: int = athlete_config.max_height) -> Page[AthleteOut]:
    
    query = select(AthleteModel).filter(AthleteModel.weight >= min_height, AthleteModel.weight <= max_height)
    results = await db_session.execute(query)
    athlete: List[AthleteOut] = results.scalars().all()

    
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Athlete not found by weight: min {min_height}, max {max_height}")

    return paginate(athlete)


@router.get(
        path = '/{id}',
        summary = "Find Athlete by ID",
        status_code = status.HTTP_200_OK,
        response_model = AthleteOut
)

async def get_athlete_by_id(id: UUID4, db_session: DatabaseDependency) -> AthleteOut:
    athlete: AthleteOut = (
        await db_session.execute(select(AthleteModel).filter_by(id = id))
    ).scalars().first()
    
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Athlete not found by id: {id}")

    return athlete

@router.patch(
        path = '/{id}',
        summary = "Edit Athlete by ID",
        status_code = status.HTTP_200_OK,
        response_model = AthleteOut
)

async def patch(
    id: UUID4,
    db_session: DatabaseDependency,
    athlete_update: AthleteUpdate = Body(...)
) -> AthleteOut:

    athlete: AthleteOut = (
        await db_session.execute(select(AthleteModel).filter_by(id = id))
    ).scalars().first()
    
    if not athlete:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Athlete not found: {id}"
        )
    athlete_update = athlete_update.model_dump(exclude_unset = True)
    for key, value in athlete_update.items():
        setattr(athlete, key, value)
    await db_session.commit()
    await db_session.refresh(athlete)
    return athlete

@router.delete(
        path = '/{id}',
        summary = "Remove athlete by ID",
        status_code = status.HTTP_204_NO_CONTENT
)

async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    athlete: AthleteOut = (
        await db_session.execute(select(AthleteModel).filter_by(id = id))
    ).scalars().first()
    
    if not athlete:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Athlete not found: {id}")
    
    await db_session.delete(athlete)
    await db_session.commit()
