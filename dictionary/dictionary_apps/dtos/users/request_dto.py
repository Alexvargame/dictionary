from dataclasses import dataclass


from dictionary.dictionary_apps.users.models import UserRole, BaseUser



@dataclass
class CreateUserDTO:
    email: str
    password: str
    username: str
    is_admin: bool
    is_active: bool
    name: str
    surname: str
    phone: str
    user_role: UserRole



