import pandas as pd
import django
import os

# Указываем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'dictionary.config.django.base')
django.setup()

from dictionary.dictionary_apps.words.models import Noun, Article, Lection, WordType

# Загружаем Excel
df = pd.read_excel("nouns_new.xlsx")

for _, row in df.iterrows():
    word = row["word"]
    word_plural = row["word_plural"]
    plural_sign = row["plural_sign"]
    word_translate = row["word_translate"]
    word_translate_plural = row["word_translate_plural"]
    article_name = row["article"]       # например "der"
    lection_name = row["lection"]       # например "Familie"
    word_type_name = row["word_type"]   # например "Noun"

    dict_article = {
        'r': 'der',
        's': 'das',
        'e': 'die',
    }
    # Находим связанные объекты
    article = Article.objects.get(name=dict_article[article_name])
    lection = Lection.objects.get(name=lection_name)
    word_type = WordType.objects.get(name=word_type_name)

    dict_article = {
        'r': 'der',
        's': 'das',
        'e': 'die',
    }
    # Создаём запись
    noun, created = Noun.objects.get_or_create(
        word=word,
        word_translate=word_translate,
        defaults={
            "word_plural": word_plural,
            "plural_sign": plural_sign,
            "word_translate_plural": word_translate_plural,
            "article": article,
            "lection": lection,
            "word_type": word_type,
        }
    )

    if created:
        print(f"✅ Добавлено слово: {word}")
    else:
        print(f"⚠️ Уже существует: {word}")
