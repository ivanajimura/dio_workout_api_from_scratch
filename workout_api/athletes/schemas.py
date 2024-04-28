from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from workout_api.categories.schemas import CategoryIn
from workout_api.contrib.schemas import BaseSchema, OutMixin
from workout_api.gyms.schemas import GymAthlete

class Athlete(BaseSchema):
    name: Annotated[str, Field(description = "Athlete\'s name", example = "João", max_length = 50)]
    cpf: Annotated[str, Field(description = "Athlete\'s CPF ", example = "12345678900", max_length = 11)]
    age: Annotated[int, Field(description = "Athlete\'s age ", example = "25")]
    weight: Annotated[PositiveFloat, Field(description = "Athlete\'s weight (kg) ", example = "75.5")]
    height: Annotated[PositiveFloat, Field(description = "Athlete\'s height (m)", example = "1.87")]
    sex: Annotated[str, Field(description = "Athlete\'s sex (m or f)", example = "f", max_length = 1)]
    category: Annotated[CategoryIn, Field(description = "Category of the athlete")]
    gym: Annotated[GymAthlete, Field(description = "Gym of the athlete")]

class AthleteIn(Athlete):
    pass

class AthleteOut(Athlete, OutMixin):
    pass

class AthleteUpdate(BaseSchema):
    name: Annotated[Optional[str], Field(None, description = "Athlete\'s name", example = "João", max_length = 50)]
    age: Annotated[Optional[int], Field(None, description = "Athlete\'s age ", example = "25")]
    weight: Annotated[Optional[PositiveFloat], Field(None, description = "Athlete\'s weight (kg) ", example = "75.5")]
    height: Annotated[Optional[PositiveFloat], Field(None, description = "Athlete\'s height (m)", example = "1.87")]
    sex: Annotated[Optional[str], Field(None, description = "Athlete\'s sex (m or f)", example = "f", max_length = 1)]