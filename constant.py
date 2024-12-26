from enum import Enum

class Collections(Enum):
    CHAT_HISTORY = "chat_history"
    DOC_RECORD = "doc_record"

    def __str__(self):
        return self.value