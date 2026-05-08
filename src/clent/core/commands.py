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
        "message": "Goodbye!",
        "action": "exit",
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
}


def commands(raw_cmd: str):
    cmd = raw_cmd.strip().lower()

    if not cmd:
        return {
            "message": "Empty command",
            "action": None,
            "error": True,
        }
        
    if cmd == "?":
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