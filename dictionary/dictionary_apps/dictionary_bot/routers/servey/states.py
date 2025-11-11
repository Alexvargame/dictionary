from aiogram.fsm.state import StatesGroup, State

class OrderRegister(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()
    waiting_for_check_password = State()

class OrderExercises(StatesGroup):
    waiting_for_exercise = State()
    waiting_for_answer = State()
    waiting_for_ids = State()
    waiting_for_selected_words = State()
    waiting_for_list_words = State()
    waiting_for_action = State()
    waiting_for_pair_words = State()
    waiting_for_tmp_left = State()
    waiting_for_tmp_right = State()


class OrderExercisesArticle(StatesGroup):
    waiting_for_exercise = State()
    waiting_for_selected_words = State()
    waiting_for_current_index = State()
    waiting_for_correct_answers = State()
    waiting_for_action_kb = State()
    waiting_for_data_kb = State()


class OrderExercisesTranslateDigits(StatesGroup):
    waiting_for_exercise = State()
    waiting_for_selected_exercises = State()
    waiting_for_current_index = State()
    waiting_for_correct_answers = State()

class OrderExercisesVerbForms(StatesGroup):
    waiting_for_exercise = State()
    waiting_for_verb_form = State()
    waiting_for_selected_verbs = State()
    waiting_for_current_index = State()
    waiting_for_correct_answers = State()


# class OrderEmployeeObjects(StatesGroup):
#     waiting_for_type_object = State()
#     waiting_for_id_object = State()
#     waiting_for_choice_flats_menu = State()
#     waiting_for_rooms_count = State()
#     waiting_for_price = State()
#     waiting_for_square = State()
#     waiting_for_category = State()
#     waiting_for_district = State()
#
#
# class OrderNewObject(StatesGroup):
#     waiting_for_type_object = State()
#     waiting_for_category_object = State()
#     waiting_for_district_object = State()
#     waiting_for_address_object = State()
#     waiting_for_rooms_count_object = State()
#     waiting_for_total_area_object = State()
#     waiting_for_living_area_object = State()
#     waiting_for_floor_object = State()
#     waiting_for_total_floor_object = State()
#     waiting_for_building_type_object = State()
#     waiting_for_repair_state_object = State()
#     waiting_for_infrastructure_object = State()
#     waiting_for_discription_object = State()
#     waiting_for_price_object = State()
#     waiting_for_title_object = State()
#     waiting_for_save_or_no_object = State()
#     waiting_for_edit_object = State()
#     waiting_for_correct_data_object = State()
