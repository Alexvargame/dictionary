import pandas as pd
import django
import os
from django.db import transaction

# Указываем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'dictionary.config.django.base')
django.setup()

from dictionary.dictionary_apps.words.models import Adjective
from dictionary.dictionary_apps.exercises.apis.dictionarys import unchangeable_adjectives


adjs = Adjective.objects.all()
with transaction.atomic():
    for adj in Adjective.objects.all():
        word_clean = adj.word.strip()
        if "stark" in adj.declensions:
            stark_dict = adj.declensions["stark"]
            existing_cases = list(stark_dict.keys())
        if adj.word not in unchangeable_adjectives:
            if "Akkusativ" in stark_dict:
                print("Akkusativ уже добавлен")
            else:
                adj.declensions['stark']['Akkusativ'] = {
                    'Maskulinum': {'den': word_clean + 'en', 'einen': word_clean + 'en'},
                    'Femininum': {'die': word_clean + 'e', 'eine': word_clean + 'e'},
                    'Neutrum': {'das': word_clean + 'es', 'ein': word_clean + 'es'},
                    'Plural': {'die': word_clean + 'e', 'keine': word_clean + 'e'}
                }
            if "Dativ" in stark_dict:
                print("Dativ уже добавлен")
            else:
                adj.declensions['stark']['Dativ'] = {
                    'Maskulinum': {'dem': word_clean + 'em', 'einem': word_clean + 'em'},
                    'Femininum': {'der': word_clean + 'er', 'einer': word_clean + 'er'},
                    'Neutrum': {'dem': word_clean + 'em', 'einem': word_clean + 'em'},
                    'Plural': {'den': word_clean + 'en', 'keinen': word_clean + 'en'}
                }
            if "Genitiv" in stark_dict:
                print("Genitiv уже добавлен")
            else:
                adj.declensions['stark']['Genitiv'] = {
                    'Maskulinum': {'des': word_clean + 'en', 'eines': word_clean + 'en'},
                    'Femininum': {'der': word_clean + 'er', 'einer': word_clean + 'er'},
                    'Neutrum': {'des': word_clean + 'en', 'eines': word_clean + 'en'},
                    'Plural': {'der': word_clean + 'er', 'keiner': word_clean + 'er'}
                }
            adj.save()
        else:
            if "Akkusativ" in stark_dict:
                print("Akkusativ уже добавлен")
            else:
                adj.declensions['stark']['Akkusativ'] = {
                    'Maskulinum': {'den': word_clean, 'einen': word_clean},
                    'Femininum': {'die': word_clean, 'eine': word_clean },
                    'Neutrum': {'das': word_clean, 'ein': word_clean},
                    'Plural': {'die': word_clean, 'keine': word_clean}
                }
            if "Dativ" in stark_dict:
                print("Dativ уже добавлен")
            else:
                adj.declensions['stark']['Dativ'] = {
                    'Maskulinum': {'dem': word_clean, 'einem': word_clean },
                    'Femininum': {'der': word_clean, 'einer': word_clean},
                    'Neutrum': {'dem': word_clean, 'einem': word_clean},
                    'Plural': {'den': word_clean, 'keinen': word_clean }
                }
            if "Genitiv" in stark_dict:
                print("Genitiv уже добавлен")
            else:
                adj.declensions['stark']['Genitiv'] = {
                    'Maskulinum': {'des': word_clean, 'eines': word_clean},
                    'Femininum': {'der': word_clean, 'einer': word_clean},
                    'Neutrum': {'des': word_clean, 'eines': word_clean},
                    'Plural': {'der': word_clean, 'keiner': word_clean}
                }
            adj.save()
