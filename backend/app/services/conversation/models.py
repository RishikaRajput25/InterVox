from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class ConversationTurn:
    turn_id: str
    user_message: str
    assistant_message: str
    created_at: datetime


@dataclass
class Conversation:
    conversation_id: str
    turns: list[ConversationTurn]

    def add_turn(
        self,
        turn_id: str,
        user_message: str,
        assistant_message: str,
    ):
        self.turns.append(
            ConversationTurn(
                turn_id=turn_id,
                user_message=user_message,
                assistant_message=assistant_message,
                created_at=datetime.now(timezone.utc),
            )
        )