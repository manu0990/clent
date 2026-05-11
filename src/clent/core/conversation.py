import json
import shutil
import uuid
from pathlib import Path
from typing import List, TypedDict


# ==========================================
# CONFIG
# ==========================================

BASE_DIR = Path(__file__).parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"


class Message(TypedDict):
    role: str
    content: str


# ==========================================
# HELPERS
# ==========================================

def load_messages(session_id: str) -> list:
    """
    Load messages from a session.
    """

    messages_file = SESSIONS_DIR / session_id / "messages.json"

    if not messages_file.exists():
        raise FileNotFoundError(f"Session '{session_id}' not found.")

    with open(messages_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_messages(
    session_id: str,
    messages: List[Message]
) -> None:
    """
    Save messages to disk.
    """

    session_dir = SESSIONS_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    messages_file = session_dir / "messages.json"

    with open(messages_file, "w", encoding="utf-8") as f:
        json.dump(
            messages,
            f,
            indent=2,
            ensure_ascii=False
        )
    


# ==========================================
# CORE
# ==========================================


def save_message(
    messages: List[Message],
    session_id: str | None = None
) -> tuple[bool, str | None]:
    """
    Create or update a session with messages.
    """

    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    # Create new session if needed
    if session_id is None:
        session_id = uuid.uuid4().hex

    session_dir = SESSIONS_DIR / session_id

    # Validate existing session
    if not session_dir.exists() and session_id is not None:
        session_dir.mkdir(parents=True, exist_ok=True)

    try:
        save_messages(session_id, messages)

        return {
            "success": True,
            "session_id": session_id
        }

    except Exception as e:
        raise RuntimeError(f"Failed to save messages: {e}") from e
    

# ==========================================
# GET MESSAGES
# ==========================================

def get_messages(
    session_id: str,
    limit: int = 30
) -> list:
    """
    Get latest messages from conversation.
    """

    messages = load_messages(session_id)

    return messages


# ==========================================
# DELETE SESSION
# ==========================================

def delete_conversation(session_id: str):
    """
    Delete conversation completely.
    """

    session_dir = SESSIONS_DIR / session_id

    if not session_dir.exists():
        raise FileNotFoundError(f"Session '{session_id}' not found.")

    try:
        shutil.rmtree(session_dir)
        print(f"Session: {session_id} cleared successfully.")

    except Exception as e:
        raise RuntimeError(f"Failed to delete session: {e}") from e


# ==========================================
# LIST CONVERSATIONS
# ==========================================

def list_all_sessions() -> list:
    """
    List all conversation ids.
    """

    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    return [
        session.name
        for session in SESSIONS_DIR.iterdir()
        if session.is_dir()
    ]


# ==========================================
# TEST
# ==========================================

# if __name__ == "__main__":

#     # create new session
#     response = save_message(
#         [{"role": "user", "content": "Hello"}]
#     )

#     session_id = response["session_id"]

#     print("\nCreated:")
#     print(response)

#     # continue session
#     save_message(
#         [{"role": "assistant", "content": "Hi there!"}],
#         session_id=session_id
#     )

#     # fetch messages
#     print("\nMessages:")
#     print(get_messages(session_id))

#     # list all sessions
#     print("\nSessions:")
#     print(list_all_sessions())

#     # delete session
#     # delete_conversation(session_id)