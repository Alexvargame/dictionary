import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram import types
from dictionary.dictionary_apps.dictionary_bot_aiogram_webhook.telegram_bot import dp, bot

@csrf_exempt
async def telegram_bot_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        update = types.Update(**data)
        await dp.feed_update(bot, update)
        return JsonResponse({"ok": True})
    return JsonResponse({"detail": "Method not allowed"}, status=405)
