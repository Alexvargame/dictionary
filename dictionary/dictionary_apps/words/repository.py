from dictionary.dictionary_apps.words.models import Word, Noun, Verb



from django.db import transaction

from dictionary.dictionary_apps.words.selectors import word_list, noun_list, verb_list
from dictionary.dictionary_apps.dtos.words.response_dto import WordDTO, NounDTO,VerbDTO
from dictionary.dictionary_apps.dtos.words.request_dto import CreateWordDTO, CreateNounDTO
from dictionary.dictionary_apps.common.services import model_update






class NounRepository:
    model = Noun
    dto = NounDTO

    @transaction.atomic
    def create_object(self, dto):
        word = self.model.objects.create(
            word=dto.word,
            word_type=dto.word_type,
            lection=dto.lection,
            word_plural=dto.word_plural,
            plural_sign=dto.plural_sign,
            word_translate=dto.word_translate,
            word_translate_plural=dto.word_translate_plural,
            article=dto.article
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
            print(dto_dictionary[obj.word_type.name]())
            tmp_dto = dto_dictionary[obj.word_type.name]().detail_object(obj)
            lst_dto.append(tmp_dto)
        return lst_dto
    @transaction.atomic
    def update_object(self, dto):

        word = self.model.objects.get(id=dto.id)
        for key, value in dto.__dict__.items():
            word.__dict__[key] = value
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)
        word.save()






class VerbRepository:
    model = Verb
    dto = VerbDTO

    @transaction.atomic
    def create_object(self, dto):
        print(' DTOOTTTT', dto)
        verb = self.model.objects.create(
            word=dto.word,
            word_type=dto.word_type,
            lection=dto.lection,
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
        for obj in noun_list(filters=filters):
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

        noun = self.model.objects.get(id=dto.id)
        for key, value in dto.__dict__.items():
           noun.__dict__[key] = value
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

        noun.save()

    @transaction.atomic
    def delete_object(self, verb_id):

        noun = self.model.objects.get(id=verb_id)
        noun.delete()
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)



dto_dictionary = {
    'Noun' : NounRepository,
    'Verb' : VerbRepository,
}






