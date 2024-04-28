from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class Category(BaseSchema):
    name: Annotated[str, Field(description = "Name of the Category", example = "Scale", max_length = 10)]

class CategoryIn(Category):
    pass

class CategoryOut(Category):
    id: Annotated[UUID4, Field(description = "Category identifier")] 