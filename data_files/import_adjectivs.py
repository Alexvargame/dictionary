import pandas as pd
import django
import os

# Указываем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'dictionary.config.django.base')
django.setup()

from dictionary.dictionary_apps.words.models import Adjective, Lection, WordType

# Загружаем Excel
df = pd.read_excel("adjectiv.xlsx")

for _, row in df.iterrows():
    word = row["word"]
    word_translate = row["word_translate"]
    komparativ = row['komparativ']
    superlativ = row['superlativ']

    # на будущее: склонение (сильное, слабое, смешанное)
    declensions = row['declensions']
    lection = row["lection"]       # например "Familie"
    #word_type = row["word_type"]   # например "Verb"

    # Находим связанные объекты
    lection = Lection.objects.get(name=lection)
    word_type = WordType.objects.get(name='Adjective')


    # Создаём запись
    adjectiv, created = Adjective.objects.get_or_create(
        word=word,
        word_translate=word_translate,
        defaults={
            "lection": lection,
            "word_type": word_type,
            "komparativ": komparativ,
            "superlativ": superlativ,
            "declensions": declensions,
            'lection': lection,
            'word_type': word_type
        }
    )

    if created:
        print(f"✅ Добавлено слово: {word}")
    else:
        print(f"⚠️ Уже существует: {word}")
