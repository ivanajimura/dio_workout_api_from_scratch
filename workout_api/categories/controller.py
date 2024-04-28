from typing import List
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.categories.schemas import CategoryIn, CategoryOut
from workout_api.categories.models import CategoryModel

from workout_api.contrib.dependencies import DatabaseDependency


router = APIRouter()

@router.post(
        path = '/',
        summary = "Add new category",
        status_code = status.HTTP_201_CREATED,
        response_model = CategoryOut
)

async def post(
    db_session: DatabaseDependency,
    category_in: CategoryIn = Body(...)
) -> CategoryOut:
    
    # Check if name already in use:
    if ((await db_session.execute(select(CategoryModel).filter_by(name = category_in.name))).scalars().first()):
        raise HTTPException(
            status_code = status.HTTP_303_SEE_OTHER,
            detail=f"Name {category_in.name} already in use"
        )

    category_out = CategoryOut(id=uuid4(), **category_in.model_dump())
    category_model = CategoryModel(**category_out.model_dump())
    db_session.add(category_model)
    await db_session.commit()
    return category_out


@router.get(
        path = '/',
        summary = "List all Categories",
        status_code = status.HTTP_200_OK,
        response_model = Page[CategoryOut]
)

async def query(db_session: DatabaseDependency) -> Page[CategoryOut]:
    categories: List[CategoryOut] = (await db_session.execute(select(CategoryModel))).scalars().all()
    
    return paginate(categories)

@router.get(
        path = '/name:{name}',
        summary = "Find Category by Name",
        status_code = status.HTTP_200_OK,
        response_model = Page[CategoryOut]
)

async def query(name: str, db_session: DatabaseDependency) -> Page[CategoryOut]:

    query = select(CategoryModel).where(CategoryModel.name.contains(name))
    results = await db_session.execute(query)
    category: List[CategoryOut] = results.scalars().all()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Category not found: {name}")

    return paginate(category)



@router.get(
        path = '/{id}',
        summary = "Find Category by ID",
        status_code = status.HTTP_200_OK,
        response_model = CategoryOut
)

async def query(id: UUID4, db_session: DatabaseDependency) -> CategoryOut:
    category: CategoryOut = (
        await db_session.execute(select(CategoryModel).filter_by(id = id))
    ).scalars().first()
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Category not found: {id}")

    return category

