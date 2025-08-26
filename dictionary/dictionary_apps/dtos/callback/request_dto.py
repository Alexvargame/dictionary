from dataclasses import dataclass


from dictionary.dictionary_apps.users.models import BaseUser



@dataclass
class CreateMessageDTO:
    user:BaseUser
    text: str
    telegram_id: int
    recipient:BaseUser
    # is_answered: bool
    # answer_text: str
    # created_at: str
    # answered_at: str



