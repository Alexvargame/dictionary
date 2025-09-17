import pandas as pd
import django
import os

# Указываем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'dictionary.config.django.base')
django.setup()

from dictionary.dictionary_apps.words.models import Numeral, Lection, WordType

# Загружаем Excel
df = pd.read_excel("numeral.xlsx")

for _, row in df.iterrows():
    word = row["word"]
    word_translate = row["word_translate"]
    ordinal = row['ordinal']
    date_numeral = row['date_numeral']
    lection = row["lection"]       # например "Familie"

    # Находим связанные объекты
    lection = Lection.objects.get(name=lection)
    word_type = WordType.objects.get(name='Numeral')


    # Создаём запись
    numeral, created = Numeral.objects.get_or_create(
        word=word,
        word_translate=word_translate,
        defaults={
            "lection": lection,
            "word_type": word_type,
            "ordinal": ordinal,
            "date_numeral": date_numeral,
            'lection': lection,
            'word_type': word_type
        }
    )

    if created:
        print(f"✅ Добавлено слово: {word}")
    else:
        print(f"⚠️ Уже существует: {word}")
