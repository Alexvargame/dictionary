import pandas as pd
import django
import os

# Указываем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'dictionary.config.django.base')
django.setup()

from dictionary.dictionary_apps.words.models import NounDeclensionsForm, Lection, WordType

# Загружаем Excel
df = pd.read_excel("other_words.xlsx")

for _, row in df.iterrows():
    word = row["word"]
    word_plural = row["word_translate"]
    lection_name = row["lection"]       # например "Familie"
    # Находим связанные объекты
    lection = Lection.objects.get(name=lection_name)
    word_type = WordType.objects.get(name='Other')
    # Создаём запись
    noun_declensions, created = NounDeclensionsForm.objects.get_or_create(
        word=word,
        word_translate=word_translate,
        defaults={
            "lection": lection,
            "word_type": word_type,
        }
    )

    if created:
        print(f"✅ Добавлено слово: {noun_declensions}")
    else:
        print(f"⚠️ Уже существует: {noun_declensions}")
