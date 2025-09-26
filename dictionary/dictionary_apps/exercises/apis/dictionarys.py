degrees_of_comparison = [
    ('komparativ'),
    ('superlativ')
]

declensions = [('stark'),]
             # ('schwach'),
             # ('gemischt')]

cases_choice = [('Nominativ')]#,'Akkusativ', 'Dativ', 'Genetiv']

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