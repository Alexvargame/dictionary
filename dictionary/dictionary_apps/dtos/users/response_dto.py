from dataclasses import dataclass
from django.forms.models import model_to_dict
from dictionary.dictionary_apps.users.models import UserRole

@dataclass
class UserDTO:
    id: int
    email: str
    password: str
    username: str
    is_admin: bool
    is_active: bool
    name: str
    surname: str
    phone: str
    user_role: UserRole
    score: float
    lifes: int
    chat_id: int
    telegram_username: str
    registration_date: str
    last_login_date: str

@dataclass
class  UserRoleDTO:
    id: int
    name: str
    description: str


# class UserDTO:
#     # предположим, у тебя __init__ ожидает эти параметры (подгони под свой)
#     def __init__(self, id, password, username, is_admin, is_active,
#                  user_role, score, lifes, chat_id,
#                  registration_date, last_login_date,
#                  name=None, surname=None, email=None, phone=None,
#                  telegram_username=None, user_bot_pass=None):
#         self.id = id
#         self.password = password
#         self.username = username
#         self.is_admin = is_admin
#         self.is_active = is_active
#         self.user_role = user_role
#         self.score = score
#         self.lifes = lifes
#         self.chat_id = chat_id
#         self.registration_date = registration_date
#         self.last_login_date = last_login_date
#         self.name = name
#         self.surname = surname
#         self.email = email
#         self.phone = phone
#         self.telegram_username = telegram_username
#         self.user_bot_pass = user_bot_pass
#
#     # === NEW: безопасный конструктор из модели Django ===
#     @classmethod
#     def from_model(cls, user_model, overrides: dict | None = None):
#         """Создаёт словарь с нужными ключами из модели user и подменяет overrides."""
#         overrides = overrides or {}
#
#         # Формируем базовый dict вручную (без _state, без неиспользуемых ключей)
#         data = {
#             "id": user_model.id,
#             "password": user_model.password,
#             "username": user_model.username,
#             "is_admin": user_model.is_admin,
#             "is_active": user_model.is_active,
#             # передаём id роли — т.к. DTO, судя по коду, ожидает id
#             "user_role": user_model.user_role.id if getattr(user_model, "user_role", None) else None,
#             "score": user_model.score if user_model.score is not None else 0,
#             "lifes": user_model.lifes if user_model.lifes is not None else 0,
#             "chat_id": user_model.chat_id if user_model.chat_id is not None else 0,
#             # у тебя в модели last_login_date, но на всякий случай fallback на last_login
#             "registration_date": user_model.registration_date,
#             "last_login_date": getattr(user_model, "last_login_date", None) or getattr(user_model, "last_login", None),
#             # editable / optional
#             "name": user_model.name or "",
#             "surname": user_model.surname or "",
#             "email": user_model.email or "",
#             "phone": user_model.phone or "",
#             "telegram_username": user_model.telegram_username or None,
#             "user_bot_pass": user_model.user_bot_pass or "",
#         }
#
#         # Подменяем только те поля, которые пришли в overrides (валидированные)
#         for k, v in overrides.items():
#             data[k] = v
#
#         # Теперь создаём DTO, полями соответствующими __init__
#         return cls(**data)
