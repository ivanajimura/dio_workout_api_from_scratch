from fastapi import APIRouter

from workout_api.athletes.controller import router as athlete
from workout_api.categories.controller import router as category
from workout_api.gyms.controller import router as gym



api_router = APIRouter()
api_router.include_router(athlete, prefix = '/athletes', tags = ['athletes'])
api_router.include_router(category, prefix = '/categories', tags = ['categories'])
api_router.include_router(gym, prefix = '/gyms', tags = ['gyms'])
