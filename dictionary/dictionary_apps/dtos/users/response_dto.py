from dataclasses import dataclass

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