from dictionary.dictionary_apps.words.models import (Word, Noun, Verb, Article,
                                                     Lection, Pronoun, Adjective,
                                                     Numeral, WordType)



from django.db import transaction

from dictionary.dictionary_apps.words.selectors import (word_list, noun_list, verb_list,
                                                        article_list, lection_list,
                                                        pronoun_list, adjective_get,
                                                        numeral_list, lection_get, word_type_get,
                                                        adjective_list)
from dictionary.dictionary_apps.dtos.words.response_dto import (WordDTO, NounDTO,VerbDTO, ArticleDTO,
                                                                LectionDTO, PronounDTO, AdjectiveDTO,
                                                                NumeralDTO)
from dictionary.dictionary_apps.dtos.words.request_dto import (CreateWordDTO, CreateNounDTO,
                                                               CreatePronounDTO, CreateAdjectiveDTO,
                                                               CreateNumeralDTO)
from dictionary.dictionary_apps.common.services import model_update






class NounRepository:
    model = Noun
    dto = NounDTO

    @transaction.atomic
    def create_object(self, dto):
        lection = Lection.objects.get(id=dto.lection)
        word_type = WordType.objects.get(id=dto.word_type)
        article = Article.objects.get(id=dto.article)
        word = self.model.objects.create(
            word=dto.word,
            word_type=word_type,
            lection=lection,
            word_plural=dto.word_plural,
            plural_sign=dto.plural_sign,
            word_translate=dto.word_translate,
            word_translate_plural=dto.word_translate_plural,
            article=article
        )
        return word

    def detail_object(self, obj):
        dto = self.dto (
            id=obj.id,
            word_type=obj.word_type,
            word=obj.word,
            word_plural=obj.word_plural,
            plural_sign=obj.plural_sign,
            word_translate=obj.word_translate,
            word_translate_plural=obj.word_translate_plural,
            article=obj.article,
            lection=obj.lection,
        )
        return dto

    def list_objects(self, filters=None):
        lst_dto = []
        print('FILR', filters)
        for obj in noun_list(filters=filters):
            tmp_dto = self.dto(
                id=obj.id,
                word_type=obj.word_type,
                word=obj.word,
                word_plural=obj.word_plural,
                plural_sign=obj.plural_sign,
                word_translate=obj.word_translate,
                word_translate_plural=obj.word_translate_plural,
                article=obj.article,
                lection=obj.lection,
            )
            lst_dto.append(tmp_dto)
        return lst_dto
    @transaction.atomic
    def update_object(self, dto):

        noun = self.model.objects.get(id=dto.id)
        for key, value in dto.__dict__.items():
           noun.__dict__[key] = value
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

        noun.save()

    @transaction.atomic
    def delete_object(self, noun_id):

        noun = self.model.objects.get(id=noun_id)
        noun.delete()
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)
class PronounRepository:
    model = Pronoun
    dto = PronounDTO

    @transaction.atomic
    def create_object(self, dto):
        lection = Lection.objects.get(id=dto.lection)
        word_type = WordType.objects.get(id=dto.word_type)
        word = self.model.objects.create(
            word = dto.word,
            word_translate = dto.word_translate,
            akkusativ = dto.akkusativ,
            akkusativ_translate = dto.akkusativ_translate,
            dativ = dto.dativ,
            dativ_translate = dto.dativ_translate,
            prossessive = dto.prossessive,
            prossessive_translate = dto.prossessive_translate,
            reflexive = dto.reflexive,
            reflexive_translate = dto.reflexive_translate,
            lection = lection,
            word_type = word_type
        )
        return word

    def detail_object(self, obj):
        dto = self.dto (
            id=obj.id,
            word=obj.word,
            word_translate=obj.word_translate,
            akkusativ=obj.akkusativ,
            akkusativ_translate=obj.akkusativ_translate,
            dativ=obj.dativ,
            dativ_translate=obj.dativ_translate,
            prossessive=obj.prossessive,
            prossessive_translate=obj.prossessive_translate,
            reflexive=obj.reflexive,
            reflexive_translate=obj.reflexive_translate,
            lection=obj.lection,
            word_type=obj.word_type
        )
        return dto

    def list_objects(self, filters=None):
        lst_dto = []
        print('FILR', filters)
        for obj in pronoun_list(filters=filters):
            tmp_dto = self.dto(
                id=obj.id,
                word=obj.word,
                word_translate=obj.word_translate,
                akkusativ=obj.akkusativ,
                akkusativ_translate=obj.akkusativ_translate,
                dativ=obj.dativ,
                dativ_translate=obj.dativ_translate,
                prossessive=obj.prossessive,
                prossessive_translate=obj.prossessive_translate,
                reflexive=obj.reflexive,
                reflexive_translate=obj.reflexive_translate,
                lection=obj.lection,
                word_type=obj.word_type
            )
            lst_dto.append(tmp_dto)
        return lst_dto
    @transaction.atomic
    def update_object(self, dto):

        pronoun = self.model.objects.get(id=dto.id)
        dto.lection = lection_get(dto.lection)
        dto.word_type = word_type_get(dto.word_type)
        for field, value in dto.__dict__.items():
            if field in [f.name for f in pronoun._meta.fields]:
                setattr(pronoun, field, value)

        pronoun.save()

    @transaction.atomic
    def delete_object(self, pronoun_id):

        pronoun = self.model.objects.get(id=pronoun_id)
        pronoun.delete()
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

class AdjectiveRepository:
    model = Adjective
    dto = AdjectiveDTO

    @transaction.atomic
    def create_object(self, dto):
        lection = Lection.objects.get(id=dto.lection)
        word_type = WordType.objects.get(id=dto.word_type)
        word = self.model.objects.create(
            word = dto.word,
            word_translate = dto.word_translate,
            komparativ = dto.komparativ,
            superlativ = dto.superlativ,
            declensions = dto.declensions,
            lection = lection,
            word_type = word_type
        )
        return word

    def detail_object(self, obj):
        dto = self.dto (
            id=obj.id,
            word=obj.word,
            word_translate=obj.word_translate,
            komparativ=obj.komparativ,
            superlativ=obj.superlativ,
            declensions=obj.declensions,
            lection=obj.lection,
            word_type=obj.word_type
        )
        return dto

    def list_objects(self, filters=None):
        lst_dto = []
        for obj in adjective_list(filters=filters):
            tmp_dto = self.dto(
                id=obj.id,
                word=obj.word,
                word_translate=obj.word_translate,
                komparativ=obj.komparativ,
                superlativ=obj.superlativ,
                declensions=obj.declensions,
                lection=obj.lection,
                word_type=obj.word_type
            )
            lst_dto.append(tmp_dto)
        return lst_dto
    @transaction.atomic
    def update_object(self, dto):
        adjective = self.model.objects.get(id=dto.id)
        dto.lection = lection_get(dto.lection)
        dto.word_type = word_type_get(dto.word_type)
        for field, value in dto.__dict__.items():
            if field in [f.name for f in adjective._meta.fields]:
                setattr(adjective, field, value)
        adjective.save()

    @transaction.atomic
    def delete_object(self, adjective_id):
        adjective = self.model.objects.get(id=adjective_id)
        adjective.delete()
class NumeralRepository:
    model = Numeral
    dto = NumeralDTO

    @transaction.atomic
    def create_object(self, dto):
        lection = Lection.objects.get(id=dto.lection)
        word_type = WordType.objects.get(id=dto.word_type)
        word = self.model.objects.create(
            word = dto.word,
            word_translate = dto.word_translate,
            ordinal = dto.ordinal,
            date_numeral = dto.date_numeral,
            lection = lection,
            word_type = word_type
        )
        return word

    def detail_object(self, obj):
        dto = self.dto (
            id=obj.id,
            word=obj.word,
            word_translate=obj.word_translate,
            ordinal=obj.ordinal,
            date_numeral=obj.date_numeral,
            lection=obj.lection,
            word_type=obj.word_type
        )
        return dto

    def list_objects(self, filters=None):
        lst_dto = []
        for obj in numeral_list(filters=filters):
            tmp_dto = self.dto(
                id=obj.id,
                word=obj.word,
                word_translate=obj.word_translate,
                ordinal=obj.ordinal,
                date_numeral=obj.date_numeral,
                lection=obj.lection,
                word_type=obj.word_type
            )
            lst_dto.append(tmp_dto)
        return lst_dto
    @transaction.atomic
    def update_object(self, dto):

        numeral = self.model.objects.get(id=dto.id)
        dto.lection = lection_get(dto.lection)
        dto.word_type = word_type_get(dto.word_type)

        for field, value in dto.__dict__.items():
            if field in [f.name for f in numeral._meta.fields]:
                setattr(numeral, field, value)
        numeral.save()


    @transaction.atomic
    def delete_object(self, numeral_id):
        numeral = self.model.objects.get(id=numeral_id)
        numeral.delete()

class WordRepository:
    model = Word
    dto = WordDTO

    @transaction.atomic
    def create_object(self, dto):
        word = self.model.objects.create(
            word_type=dto.word_type,
            lection=dto.lection,

        )
        return word

    def detail_object(self, obj):
        dto = self.dto (
            id=obj.id,
            word_type=obj.word_type,
            lection=obj.lection,
        )
        return dto

    def list_objects(self, filters=None):
        lst_dto = []
        filtered_objects = [obj for obj in word_list(filters=filters) if type(obj) is not Word]
        for obj in filtered_objects:
            # print(obj.word_type.name)
            tmp_dto = dto_dictionary[obj.word_type.name]().detail_object(obj)
            lst_dto.append(tmp_dto)
        return lst_dto
    @transaction.atomic
    def update_object(self, dto):
        word = self.model.objects.get(id=dto.id)
        for key, value in dto.__dict__.items():
            if field in [f.name for f in obj._meta.fields]:
                setattr(obj, field, value)
           # word.__dict__[key] = value
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)
        word.save()






class VerbRepository:
    model = Verb
    dto = VerbDTO

    @transaction.atomic
    def create_object(self, dto):
        lection = Lection.objects.get(id=dto.lection)
        word_type = WordType.objects.get(id=dto.word_type)
        verb = self.model.objects.create(
            word=dto.word,
            word_type=word_type,
            lection=lection,
            word_translate=dto.word_translate,
            ich_form=dto.ich_form,
            du_form=dto.du_form,
            er_sie_es_form=dto.er_sie_es_form,
            wir_form=dto.wir_form,
            ihr_form=dto.ihr_form,
            Sie_sie_form=dto.Sie_sie_form,
            past_perfect_form=dto.past_perfect_form,
            past_prateritum_ich_form=dto.past_prateritum_ich_form,
            past_prateritum_du_form=dto.past_prateritum_du_form,
            past_prateritum_er_sie_es_form=dto.past_prateritum_er_sie_es_form,
            past_prateritum_wir_form=dto.past_prateritum_wir_form,
            past_prateritum_ihr_form=dto.past_prateritum_ihr_form,
            past_prateritum_Sie_sie_form=dto.past_prateritum_Sie_sie_form,
        )
        return verb

    def detail_object(self, obj):
        dto = self.dto (
            id=obj.id,
            word_type=obj.word_type,
            lection=obj.lection,
            word=obj.word,
            word_translate=obj.word_translate,
            ich_form=obj.ich_form,
            du_form=obj.du_form,
            er_sie_es_form=obj.er_sie_es_form,
            wir_form=obj.wir_form,
            ihr_form=obj.ihr_form,
            Sie_sie_form=obj.Sie_sie_form,
            past_perfect_form=obj.past_perfect_form,
            past_prateritum_ich_form=obj.past_prateritum_ich_form,
            past_prateritum_du_form=obj.past_prateritum_du_form,
            past_prateritum_er_sie_es_form=obj.past_prateritum_er_sie_es_form,
            past_prateritum_wir_form=obj.past_prateritum_wir_form,
            past_prateritum_ihr_form=obj.past_prateritum_ihr_form,
            past_prateritum_Sie_sie_form=obj.past_prateritum_Sie_sie_form,
        )
        return dto

    def list_objects(self, filters=None):
        lst_dto = []
        for obj in verb_list(filters=filters):
            tmp_dto = self.dto(
                id=obj.id,
                word_type=obj.word_type,
                lection=obj.lection,
                word=obj.word,
                word_translate=obj.word_translate,
                ich_form=obj.ich_form,
                du_form=obj.du_form,
                er_sie_es_form=obj.er_sie_es_form,
                wir_form=obj.wir_form,
                ihr_form=obj.ihr_form,
                Sie_sie_form=obj.Sie_sie_form,
                past_perfect_form=obj.past_perfect_form,
                past_prateritum_ich_form=obj.past_prateritum_ich_form,
                past_prateritum_du_form=obj.past_prateritum_du_form,
                past_prateritum_er_sie_es_form=obj.past_prateritum_er_sie_es_form,
                past_prateritum_wir_form=obj.past_prateritum_wir_form,
                past_prateritum_ihr_form=obj.past_prateritum_ihr_form,
                past_prateritum_Sie_sie_form=obj.past_prateritum_Sie_sie_form,
            )
            lst_dto.append(tmp_dto)
        return lst_dto
    @transaction.atomic
    def update_object(self, dto):

        verb = self.model.objects.get(id=dto.id)
        for field, value in dto.__dict__.items():
            if field in [f.name for f in obj._meta.fields]:
                setattr(obj, field, value)
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)
        verb.save()

    @transaction.atomic
    def delete_object(self, verb_id):

        noun = self.model.objects.get(id=verb_id)
        noun.delete()
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)


class ArticleRepository:
    model = Article
    dto = ArticleDTO

    def list_objects(self, filters=None):
        lst_dto = []
        for obj in article_list(filters=filters):
            tmp_dto = self.dto(
                id=obj.id,
                name=obj.name,
                description=obj.description,
            )
            lst_dto.append(tmp_dto)
        return lst_dto



class LectionRepository:
    model = Lection
    dto = LectionDTO

    def list_objects(self, filters=None):
        lst_dto = []
        for obj in lection_list(filters=filters):
            tmp_dto = self.dto(
                id=obj.id,
                name=obj.name,
                book=obj.book,
                description=obj.description,
            )
            lst_dto.append(tmp_dto)
        return lst_dto


dto_dictionary = {
    'Noun' : NounRepository,
    'Verb' : VerbRepository,
    'Numeral': NumeralRepository,
    'Adjective': AdjectiveRepository,
    'Pronoun': PronounRepository,
}






