degrees_of_comparison = [
    ('komparativ'),
    ('superlativ')
]

declensions = [('stark'),]
             # ('schwach'),
             # ('gemischt')]

cases_choice = [('Nominativ'),('Akkusativ'), ('Dativ'), ('Genitiv')]

gender = {'M': {'Maskulinum': 'der'},
          'F': {'Femininum': 'die'},
          'N': {'Neutrum': 'das'},
          'PL': {'Plural': 'die'},
          }
articles = {
    'der': 'Maskulinum',
    'das': 'Neutrum',
    'die': 'Femininum'
}
casus_articles = {
    "ein": [
        "ein", "eine", "einen", "einem", "eines", "einer"],
    "kein": [
        "kein", "keine", "keinen", "keinem", "keines", "keiner"],
    "definite": [
        "der", "die", "das", "den", "dem", "des"]
}


# nouns_by_case = {
#     "Mann": {
#         "Nominativ": "Mann",
#         "Genitiv": "Mannes",
#         "Dativ": "Mann",
#         "Akkusativ": "Mann",
#         "Plural Nominativ": "Männer",
#         "Plural Genitiv": "Männer",
#         "Plural Dativ": "Männern",
#         "Plural Akkusativ": "Männer"
#     },
#     "Frau": {
#         "Nominativ": "Frau",
#         "Genitiv": "Frau",
#         "Dativ": "Frau",
#         "Akkusativ": "Frau",
#         "Plural Nominativ": "Frauen",
#         "Plural Genitiv": "Frauen",
#         "Plural Dativ": "Frauen",
#         "Plural Akkusativ": "Frauen"
#     },
#     "Kind": {
#         "Nominativ": "Kind",
#         "Genitiv": "Kindes",
#         "Dativ": "Kind",
#         "Akkusativ": "Kind",
#         "Plural Nominativ": "Kinder",
#         "Plural Genitiv": "Kinder",
#         "Plural Dativ": "Kindern",
#         "Plural Akkusativ": "Kinder"
#     },
#     "Leute": {
#         "Nominativ": "Leute",
#         "Genitiv": "Leute",
#         "Dativ": "Leuten",
#         "Akkusativ": "Leute"
#     }
# }

# 2. Словарь: слово -> список всех форм без повторов
nouns_forms = {
    "Mann": ["Mann", "Mannes", "Männer", "Männern"],
    "Frau": ["Frau", "Frauen"],
    "Kind": ["Kind", "Kindes", "Kinder", "Kindern"],
    "Leute": ["Leute", "Leuten"]
}

unchangeable_adjectives = [
    "rosa", "lila", "beige", "orange", "khaki", "creme",
    "lavendel", "malve", "oliv", "aquamarin", "pink", "violett",
    "türkis", "magenta",  "cyan", "indigo", "silber", "gold",
    "cool", "neutral", "casual", "sexy", "mini", "top", "super",
    "mokka", "petrol",  "coral", "beige", "orange", "rosa", "lila", "mauve", "cyan", "fuchsia", "türkis", "magenta", "aqua",
    "chic", "cool", "trendy", "retro", "vintage", "stylish", "modern", "urban",
    "violett", "blaugrün", "hellblau", "dunkelrot"
]
# add_dict_akk = {'Maskulinum': {'den': '', 'einen': ''}, 'Femininum': {'die': '', 'eine': ''},
#             'Neutrum': {'das': '', 'ein': ''}, 'Plural': {'die': '', 'keine': ''}}
# add_dict_dat = {'Maskulinum': {'dem': '', 'einem': ''}, 'Femininum': {'der': '', 'einer': ''},
#             'Neutrum': {'dem': '', 'einem': ''}, 'Plural': {'den': '', 'keinen': ''}}
# add_dict_gen = {'Maskulinum': {'des': '', 'eines': ''}, 'Femininum': {'der': '', 'einer': ''},
#             'Neutrum': {'des': '', 'eines': ''}, 'Plural': {'der': '', 'keiner': ''}}
# add_dict_akk_form = {'Maskulinum': {'den': 'en', 'einen': 'en'}, 'Femininum': {'die': 'e', 'eine': 'e'},
#             'Neutrum': {'das': 'es', 'ein': 'es'}, 'Plural': {'die': 'e', 'keine': 'e'}}
# add_dict_dat_form = {'Maskulinum': {'dem': 'em', 'einem': 'em'}, 'Femininum': {'der': 'er', 'einer': 'er'},
#             'Neutrum': {'dem': 'em', 'einem': 'em'}, 'Plural': {'den': 'en', 'keinen': 'en'}}
# add_dict_gen_form = {'Maskulinum': {'des': 'en', 'eines': 'en'}, 'Femininum': {'der': 'er', 'einer': 'er'},
#             'Neutrum': {'des': 'en', 'eines': 'en'}, 'Plural': {'der': 'er', 'keiner': 'er'}}