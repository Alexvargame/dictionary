from asgiref.sync import sync_to_async
from django.utils import timezone


async def count_score_lifes(user, correct_answers, questions):

    if correct_answers < questions:
        user.lifes -= 1
    user.score += correct_answers
    print(user.score, user.lifes)
    await sync_to_async(user.save)()

async def user_last_update(user):
    now_update = timezone.now()
    user.last_login_date = now_update
    await sync_to_async(user.save)()


