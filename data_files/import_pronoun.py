import pandas as pd
import django
import os

# Указываем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'dictionary.config.django.base')
django.setup()

from dictionary.dictionary_apps.words.models import Pronoun, Article, Lection, WordType

# Загружаем Excel
df = pd.read_excel("pronoun.xlsx")

for _, row in df.iterrows():
    word = row["word"]
    word_translate = row["word_translate"]
    akkusativ = row['akkusativ']
    akkusativ_translate = row['akkusativ_translate']
    dativ = row['dativ']
    dativ_translate = row['dativ_translate']
    prossessive = row['prossessive']
    prossessive_translate = row['prossessive_translate']
    reflexive = row['reflexive']
    reflexive_translate = row['reflexive_translate']
    lection_name = row["lection"]       # например "Familie"

    # Находим связанные объекты
    lection = Lection.objects.get(name=lection_name)
    word_type = WordType.objects.get(name='Pronoun')

    # Создаём запись
    pronoun, created = Pronoun.objects.get_or_create(
        word=word,
        word_translate=word_translate,
        defaults={
            "akkusativ": akkusativ,
            "akkusativ_translate": akkusativ_translate,
            "dativ": dativ,
            "dativ_translate": dativ_translate,
            "prossessive": prossessive,
            "prossessive_translate": prossessive_translate,
            "reflexive": reflexive,
            "reflexive_translate": reflexive_translate,
            "lection": lection,
            "word_type": word_type,
        }
    )

    if created:
        print(f"✅ Добавлено слово: {word}")
    else:
        print(f"⚠️ Уже существует: {word}")
