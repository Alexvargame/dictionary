import pandas as pd
import django
import os

# Указываем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'dictionary.config.django.base')
django.setup()

from dictionary.dictionary_apps.words.models import Verb, Lection, WordType

# Загружаем Excel
df = pd.read_excel("german_verbs_6.xlsx")

for _, row in df.iterrows():
    word = row["word"]
    word_translate = row["word_translate"]
    ich_form = row['ich_form']
    du_form = row['du_form']
    er_sie_es_form = row['er_sie_es_form']
    wir_form = row['wir_form']
    ihr_form = row['ihr_form']
    Sie_sie_form = row['Sie_sie_form']
    past_perfect_form = row['past_perfect_form']
    past_prateritum_ich_form = row['past_prateritum_ich_form']
    past_prateritum_du_form = row['past_prateritum_du_form']
    past_prateritum_er_sie_es_form = row['past_prateritum_er_sie_es_form']
    past_prateritum_wir_form = row['past_prateritum_wir_form']
    past_prateritum_ihr_form = row['past_prateritum_ihr_form']
    past_prateritum_Sie_sie_form = row['past_prateritum_Sie_sie_form']
    regal = row['regal']
    lection = row["lection"]       # например "Familie"
    #word_type = row["word_type"]   # например "Verb"

    # Находим связанные объекты
    lection = Lection.objects.get(name=lection)
    word_type = WordType.objects.get(name='Verb')


    # Создаём запись
    verb, created = Verb.objects.get_or_create(
        word=word,
        word_translate=word_translate,
        defaults={
            "lection": lection,
            "word_type": word_type,
            'ich_form': ich_form,
            'du_form': du_form,
            'er_sie_es_form': er_sie_es_form,
            'wir_form': wir_form,
            'ihr_form': ihr_form,
            'Sie_sie_form': Sie_sie_form,
            'past_perfect_form': past_perfect_form,
            'past_prateritum_ich_form': past_prateritum_ich_form,
            'past_prateritum_du_form': past_prateritum_du_form,
            'past_prateritum_er_sie_es_form': past_prateritum_er_sie_es_form,
            'past_prateritum_wir_form': past_prateritum_wir_form,
            'past_prateritum_ihr_form': past_prateritum_ihr_form,
            'past_prateritum_Sie_sie_form': past_prateritum_Sie_sie_form,
            'regal': regal,
            'lection': lection,
            'word_type': word_type
        }
    )

    if created:
        print(f"✅ Добавлено слово: {word}")
    else:
        print(f"⚠️ Уже существует: {word}")
