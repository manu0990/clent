def help_command():
    lines = []

    for name, cmd in COMMANDS.items():
        lines.append(f"/{name} - {cmd['description']}")

    return {
        "message": "\n".join(lines),
        "action": None,
    }

def bye_command():
    return {
        "message": "Goodbye!\n",
        "action": "exit",
    }

def list_sessions_command():
    return {
        "message": "Available sessions:\n",
        "action": "list_sessions",
    }

def delete_session_command():
    return {
        "message": "",
        "action": "clear",
    }

def new_chat_command():
    return {
        "message": "Starting a new chat...\n",
        "action": "new_chat",
    }


COMMANDS = {
    "help": {
        "handler": help_command,
        "description": "Show available commands",
    },

    "bye": {
        "handler": bye_command,
        "description": "Exit the app",
    },

    "new-chat": {
        "handler": new_chat_command,
        "description": "Create a new session and start chatting",
    },
    "sessions": {
        "handler": list_sessions_command,
        "description": "List all available sessions",
    },
    "clear": {
        "handler": delete_session_command,
        "description": "Delete current session history",
    },
}


def commands(raw_cmd: str, session_id: str = None) -> dict:
    cmd = raw_cmd.strip().lower()

    if not cmd:
        return {
            "message": "Empty command",
            "action": None,
            "error": True,
        }
        
    if cmd == "?" or cmd == "help":
        print("Available commands:")
        cmd = "help"

    command = COMMANDS.get(cmd)

    if not command:
        return {
            "message": f"Unknown command: {cmd}",
            "action": None,
            "error": True,
        }

    return command["handler"]()