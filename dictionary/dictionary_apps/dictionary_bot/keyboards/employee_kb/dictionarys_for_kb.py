from .main_employee_kb import build_admin_kb, build_employee_kb
from .exercises_kb import build_exercises_kb

kb_dict_cancel = {
        'next_cancel:cancel': {
            'A': build_exercises_kb,
            'E': build_exercises_kb,
        },
        'exercises:cancel': {
            'A': build_admin_kb,
            'E': build_employee_kb,
        },
        'translate_words:cancel':{
            'A': build_exercises_kb,
            'E': build_exercises_kb,
        },
        'translate_digits:cancel':{
            'A': build_exercises_kb,
            'E': build_exercises_kb,
        },
        'verb_forms:cancel':{
            'A': build_exercises_kb,
            'E': build_exercises_kb,
        },
        'articles:cancel':{
            'A': build_exercises_kb,
            'E': build_exercises_kb,
        },
        'admin:cancel': {
            'A': build_admin_kb,
            'E': build_employee_kb,
        },
        'employee:cancel': {
            'A': build_admin_kb,
            'E': build_employee_kb,
        },
        'perfect_forms:cancel': {
            'A': build_admin_kb,
            'E': build_employee_kb,
        },
        'pronouns:cancel': {
            'A': build_admin_kb,
            'E': build_employee_kb,
        },
    }