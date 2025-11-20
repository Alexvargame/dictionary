from aiogram import Router

from .handlers_translate_words import router as translate_words_router
from .handlers_articles import router as article_router
from .handlers_translate_digits import router as translate_digits_router
from .handlers_verb_forms import router as verb_forms_router
from .handlers_pronouns import router as pronoun_router

router = Router(name='exercises')

router.include_routers(
   translate_words_router,
   article_router,
   translate_digits_router,
   verb_forms_router,
   pronoun_router,
)
