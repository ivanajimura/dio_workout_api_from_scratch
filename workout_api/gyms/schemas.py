from typing import Annotated
from pydantic import UUID4,Field
from workout_api.contrib.schemas import BaseSchema


class Gym(BaseSchema):
    name: Annotated[str, Field(description = "Name of the Gym", example = "Casa de Pedra", max_length = 20)]
    address: Annotated[str, Field(description = "Address of the Gym", example = "Rua Venancio Aires, 600", max_length = 60)]
    owner: Annotated[str, Field(description = "Name of the owner the Gym", example = "Alexandre Pedra", max_length = 30)]
    
class GymAthlete(BaseSchema):
    name: Annotated[str, Field(description = "Name of the Gym", example = "Casa de Pedra", max_length = 20)]

class GymIn(Gym):
    pass

class GymOut(Gym):
    id: Annotated[UUID4, Field(description = "Gym identifier")] 