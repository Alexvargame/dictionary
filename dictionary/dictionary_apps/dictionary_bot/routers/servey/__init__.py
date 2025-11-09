from aiogram import Router

from .handlers_reg_auth import router as reg_auth_handlers_router
from .handlers_choice_exercises import router as choice_exercise_router
from .handlers_exercises import router as exercises_router


router = Router(name='survey')

router.include_routers(
   reg_auth_handlers_router,
   choice_exercise_router,
   exercises_router,
)
