from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from workout_api.contrib.models import BaseModel
import workout_api.categories.config as category_config

class CategoryModel(BaseModel):
    __tablename__ = 'categories'
    pk_id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(category_config.name_max_length), unique = True, nullable = False)
    athlete: Mapped["AthleteModel"] = relationship(back_populates = "category")

    