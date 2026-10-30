import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dictionary.config.django.base")
django.setup()

# дальше твои импорты моделей

from django.core.management.base import BaseCommand
from dictionary.dictionary_apps.words.models import SentenceBuild



SENTENCES = [
    ("Ich gehe heute in die Schule.", "Я иду сегодня в школу.",
     "Простое повествовательное. Глагол `gehe` на 2-м месте (Verbzweitstellung).", "simple"),
    ("Heute gehe ich in die Schule.", "Сегодня я иду в школу.",
     "Обстоятельство `Heute` на 1-м месте, глагол `gehe` остаётся на 2-м. Инверсия.", "inversion"),
    ("Ich kann heute nicht kommen.", "Я не могу сегодня прийти.",
     "Satzklammer: `kann` на 2-м месте, инфинитив `kommen` в конце.", "modal"),
    ("Kannst du mir helfen?", "Ты можешь мне помочь?",
     "Вопрос без W-Wort: глагол `kannst` на 1-м месте (Verberststellung).", "question_yesno"),
    ("Wo wohnst du?", "Где ты живёшь?",
     "W-Wort `Wo` на 1-м месте, глагол `wohnst` на 2-м (Verbzweitstellung).", "question_w"),
    ("Ich weiß, dass er morgen kommt.", "Я знаю, что он придёт завтра.",
     "Придаточное с `dass`: глагол `kommt` в конце (Verbendstellung).", "complex"),
    ("Ich bleibe zu Hause, weil es regnet.", "Я остаюсь дома, потому что идёт дождь.",
     "Придаточное с `weil`: глагол `regnet` в конце (Verbendstellung).", "complex"),
    ("Wenn es regnet, bleibe ich zu Hause.", "Если идёт дождь, я остаюсь дома.",
     "`wenn` на 1-м месте, `regnet` в конце. В главном — инверсия: `bleibe` перед `ich`.", "complex"),
    ("Ich lese ein Buch, und er schreibt einen Brief.", "Я читаю книгу, а он пишет письмо.",
     "Сложносочинённое с `und`. В обеих частях глагол на 2-м месте.", "compound"),
    ("Geh jetzt nach Hause!", "Иди сейчас домой!",
     "Imperativ: глагол `Geh` на 1-м месте (Verberststellung).", "imperative"),
]


def main():
    created = 0
    skipped = 0
    for text, translate, comment, level in SENTENCES:
        obj, was_created = SentenceBuild.objects.get_or_create(
            text=text,
            defaults={"translate": translate, "comment": comment, "level": level},
        )
        if was_created:
            created += 1
            print(f"+ {obj.text}")
        else:
            skipped += 1
            print(f"= уже есть: {obj.text}")

    print(f"\nСоздано: {created}, пропущено: {skipped}, всего в базе: {SentenceBuild.objects.count()}")


if __name__ == "__main__":
    main()