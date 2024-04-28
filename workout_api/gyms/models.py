from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from workout_api.contrib.models import BaseModel
from datetime import datetime
from sqlalchemy import DateTime, Integer, String
import workout_api.gyms.config as gym_config

class GymModel(BaseModel):
    __tablename__ = 'gyms'
    pk_id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(gym_config.name_max_length), unique = True, nullable = False)
    address: Mapped[str] = mapped_column(String(gym_config.address_max_length), nullable = False)
    owner: Mapped[str] = mapped_column(String(gym_config.owner_max_length), nullable = False)
    athlete: Mapped["AthleteModel"] = relationship(back_populates = "gym")
    #created_at: Mapped[datetime] = mapped_column(DateTime, nullable = False)