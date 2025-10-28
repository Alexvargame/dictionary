from dataclasses import dataclass
from typing import Dict
from dictionary.dictionary_apps.users.models import BaseUser
@dataclass
class MessagerDTO:
    id: int
    user: BaseUser
    text: str
    is_answered: bool
    answer_text: str
    created_at: str
    answered_at: str
    telegram_id: int
    recipient: BaseUser

@dataclass
class QwizDTO:
    id: int
    user:BaseUser
    poll_id: int
    question: str
    options: Dict
    answer_text: int
    created_at: str
    correct_answer: int
    recipient:BaseUser
