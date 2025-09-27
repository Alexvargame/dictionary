from django.db import models
from model_utils.managers import InheritanceManager

class Book(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.name

class Lection(models.Model):
    name = models.CharField(max_length=30)
    book = models.ForeignKey(Book, related_name='lections', verbose_name='книга',on_delete=models.CASCADE, default=1)
    description = models.TextField()

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'

    def __str__(self):
        #return f'{self.book}:{self.name}'
        return f'{self.name}'


class Article(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField()
    forms = models.JSONField(default=dict, verbose_name="Формы", blank=True, null=True)

    class Meta:
        verbose_name = 'Артикль'
        verbose_name_plural = 'Артикли'

    def __str__(self):
        return self.name

class WordType(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Тип слова'
        verbose_name_plural = 'Типы слов'

    def __str__(self):
        return self.name

class Word(models.Model):

    word_type = models.ForeignKey(WordType, verbose_name='Тип слова', related_name='types',
                             on_delete=models.CASCADE, default=1)
    lection = models.ForeignKey(Lection, verbose_name='Лекция', related_name='lection',
                                on_delete=models.CASCADE, default=1)

    objects = InheritanceManager()  # ← это главное

    class Meta:
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'

    def __str__(self):
        return f"{self.word_type}"
#
class Noun(Word):
    word = models.CharField(max_length=30, verbose_name="Существительное")
    word_translate = models.CharField(max_length=30, verbose_name='Перевод')
    word_plural = models.CharField(max_length=30, blank=True, null=True)
    plural_sign = models.CharField(max_length=5, blank=True, null=True)
    word_translate_plural = models.CharField(max_length=30, blank=True, null=True)
    article = models.ForeignKey(Article, verbose_name='Артикль', related_name='arcticle',
                                on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Существительное'
        verbose_name_plural = 'Существительные'

    def __str__(self):
        return f"{self.word_type}: {self.id}"
#
class Verb(Word):
    word = models.CharField(max_length=30, verbose_name="Глагол")
    word_translate = models.CharField(max_length=30, verbose_name='Перевод')
    ich_form = models.CharField(max_length=30)
    du_form = models.CharField(max_length=30)
    er_sie_es_form = models.CharField(max_length=30)
    wir_form = models.CharField(max_length=30)
    ihr_form = models.CharField(max_length=30)
    Sie_sie_form = models.CharField(max_length=30)
    past_perfect_form = models.CharField(max_length=30, blank=True, null=True)
    past_prateritum_ich_form = models.CharField(max_length=30, blank=True, null=True)
    past_prateritum_du_form = models.CharField(max_length=30, blank=True, null=True)
    past_prateritum_er_sie_es_form = models.CharField(max_length=30, blank=True, null=True)
    past_prateritum_wir_form = models.CharField(max_length=30, blank=True, null=True)
    past_prateritum_ihr_form = models.CharField(max_length=30, blank=True, null=True)
    past_prateritum_Sie_sie_form = models.CharField(max_length=30, blank=True, null=True)
    regal = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Глагол'
        verbose_name_plural = 'Глаголы'

    def __str__(self):
        return f'{self.word_type}: {self.id}'


class Adjective(Word):
    word = models.CharField(max_length=30, verbose_name="Прилагательное")
    word_translate = models.CharField(max_length=50, verbose_name="Перевод")

    # степени сравнения
    komparativ = models.CharField(max_length=30, blank=True, null=True, verbose_name="Сравнительная степень")
    superlativ = models.CharField(max_length=30, blank=True, null=True, verbose_name="Превосходная степень")

    # на будущее: склонение (сильное, слабое, смешанное)
    declensions = models.JSONField(default=dict, blank=True, null=True, verbose_name="Склонение")

    class Meta:
        verbose_name = "Прилагательное"
        verbose_name_plural = "Прилагательные"

    def __str__(self):
        return f'{self.word}: {self.id}'
class Numeral(Word):
    word = models.CharField(max_length=30, verbose_name="Числительное")
    word_translate = models.CharField(max_length=50, verbose_name="Перевод")
    ordinal = models.CharField(max_length=30, blank=True, null=True, verbose_name="Прорядковый")
    date_numeral = models.CharField(max_length=30, blank=True, null=True, verbose_name="Для даты")
    class Meta:
        verbose_name = "Числительное"
        verbose_name_plural = "Числительные"

    def __str__(self):
        return f'{self.word}: {self.id}'

class Pronoun(Word):
    word = models.CharField(max_length=30, verbose_name="Местоимение")
    word_translate = models.CharField(max_length=50, verbose_name="Перевод")
    akkusativ = models.CharField(max_length=30, blank=True, null=True, verbose_name="Винительный падеж")
    akkusativ_translate = models.CharField(max_length=30, blank=True, null=True, verbose_name="Перевод винительный падеж")
    dativ = models.CharField(max_length=30, blank=True, null=True, verbose_name="Дательный падеж")
    dativ_translate = models.CharField(max_length=30, blank=True, null=True, verbose_name="Перевод дательный падеж")
    prossessive = models.CharField(max_length=30, blank=True, null=True, verbose_name="Притяжательное")
    prossessive_translate = models.CharField(max_length=30, blank=True, null=True, verbose_name="Перевод притяжательное")
    reflexive = models.CharField(max_length=30, blank=True, null=True, verbose_name="Возвратное")
    reflexive_translate = models.CharField(max_length=30, blank=True, null=True, verbose_name="Перевод возвратное")
    class Meta:
        verbose_name = "Местоимение"
        verbose_name_plural = "Местоимения"

    def __str__(self):
        return f'{self.word}: {self.id}'

class OtherWords(Word):
    word = models.CharField(max_length=30, verbose_name="Существительное")
    word_translate = models.CharField(max_length=30, verbose_name='Перевод')

    class Meta:
        verbose_name = 'Остальное слово'
        verbose_name_plural = 'Остальные слова'
    def __str__(self):
        return f"{self.word_type}: {self.id}"

class NounDeclensionsForm(models.Model):

    noun = models.ForeignKey(Noun, related_name='declension_forms', on_delete=models.CASCADE)
    nominativ = models.CharField(max_length=30, blank=True, null=True, default='')
    genitiv = models.CharField(max_length=30, blank=True, null=True, default='')
    dativ = models.CharField(max_length=30, blank=True, null=True, default='')
    akkusativ = models.CharField(max_length=30, blank=True, null=True, default='')
    plural_nominativ = models.CharField(max_length=30, blank=True, null=True, default='')
    plural_genitiv = models.CharField(max_length=30, blank=True, null=True, default='')
    plural_dativ = models.CharField(max_length=30, blank=True, null=True, default='')
    plural_akkusativ = models.CharField(max_length=30, blank=True, null=True, default='')

    class Meta:
        verbose_name = "Склонение существительного"
        verbose_name_plural = "Склонения существительного"

    def __str__(self):
        return f'{self.noun}: {self.id}'