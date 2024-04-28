from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from workout_api.contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

import workout_api.athletes.config as athlete_config

class AthleteModel(BaseModel):
    __tablename__ = 'athletes'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(athlete_config.name_max_length), nullable = False)
    cpf: Mapped[str] = mapped_column(String(11), unique = True, nullable = False)
    age: Mapped[int] = mapped_column(Integer, nullable = False)
    weight: Mapped[float] = mapped_column(Float, nullable = False)
    height: Mapped[float] = mapped_column(Float, nullable = False)
    sex: Mapped[str] = mapped_column(String(1), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable = False)
    category: Mapped["CategoryModel"] = relationship(back_populates = "athlete", lazy = "selectin")
    category_id : Mapped[int] = mapped_column(ForeignKey("categories.pk_id"))
    gym: Mapped["GymModel"] = relationship(back_populates = "athlete", lazy = "selectin")
    gym_id : Mapped[int] = mapped_column(ForeignKey("gyms.pk_id"))