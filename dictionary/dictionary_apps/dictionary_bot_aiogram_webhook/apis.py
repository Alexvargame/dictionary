


































import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram import types
from dictionary.dictionary_apps.dictionary_bot_aiogram_webhook.telegram_bot import dp, bot
from dictionary.dictionary_apps.dictionary_bot_aiogram_webhook.aiogram_loop import aiogram_loop
import asyncio

@csrf_exempt
async def telegram_bot_webhook(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    update = types.Update(**data)

    # Отправляем update в отдельный loop, который не закрывается
    await asyncio.wrap_future(
        asyncio.run_coroutine_threadsafe(
            dp.feed_update(bot, update),
            aiogram_loop
        )
    )

    return JsonResponse({"ok": True})
# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from aiogram import types
# from dictionary.dictionary_apps.dictionary_bot_aiogram_webhook.telegram_bot import dp, bot
#
# @csrf_exempt
# async def telegram_bot_webhook(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         update = types.Update(**data)
#         await dp.feed_update(bot, update)
#         return JsonResponse({"ok": True})
#     return JsonResponse({"detail": "Method not allowed"}, status=405)

#
# from asgiref.sync import async_to_sync
#
# def telegram_bot_webhook(request):
#     update = json.loads(request.body)
#     # feed_update вызываем синхронно через async_to_sync
#     async_to_sync(dp.feed_update)(bot, update)
#     return JsonResponse({"ok": True})