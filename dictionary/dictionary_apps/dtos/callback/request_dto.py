from dataclasses import dataclass
from typing import Dict

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

@dataclass
class CreateQwizDTO:
    user:BaseUser
    poll_id: int
    question: str
    options: Dict
    #answer_text: int
    correct_answer:int
    recipient:BaseUser

