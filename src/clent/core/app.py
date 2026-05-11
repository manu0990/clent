from .commands import commands
from .chat import ChatStream
from ..prompts.system_prompt import SYSTEM_PROMPT
from .conversation import get_messages, save_message, delete_conversation, list_all_sessions


def app():
    global CURRENT_SESSION_ID
    CURRENT_SESSION_ID = None
    global messages
    messages = [SYSTEM_PROMPT]

    if CURRENT_SESSION_ID:
        messages.extend(get_messages(CURRENT_SESSION_ID))

    try:
        while True:
            user_input = input("\n➤  ")

            if not user_input:
                continue

            # command mode
            if user_input.startswith("/") or user_input == "?":
                result = (
                    commands(user_input[1:], session_id=CURRENT_SESSION_ID)
                    if user_input.startswith("/")
                    else commands("?")
                )

                if result["message"]:
                    print(result["message"])

                if result["action"] == "exit":
                    break

                if result["action"] == "new_chat":
                    CURRENT_SESSION_ID = None
                    messages = [SYSTEM_PROMPT]
                    print("Started a new chat session.")

                if result["action"] == "clear":
                    delete_conversation(CURRENT_SESSION_ID)
                    CURRENT_SESSION_ID = None
                    messages = [SYSTEM_PROMPT]
                
                if result["action"] == "list_sessions":
                    sessions = list_all_sessions()
                    if not sessions:
                        print("No sessions found.")
                    else:
                        print("Available sessions:\n" + "\n".join(f"- {s}" for s in sessions))
                
                continue

            # llm mode
            print("✤  ", end="", flush=True)
            try:
                messages.append({"role": "user", "content": user_input})

                full_response = ""
                for text in ChatStream(messages):
                    print(text, end="", flush=True)
                    full_response += text

                messages.append({"role": "assistant", "content": full_response.strip()})
                msg_res = save_message(messages=messages[1:], session_id=CURRENT_SESSION_ID)

                if not CURRENT_SESSION_ID and msg_res["success"] and msg_res["session_id"]:
                    CURRENT_SESSION_ID = msg_res["session_id"]

            except Exception as exc:
                print(f"\n\nError: {exc}\n", end="")
                break
            finally:
                print("\n")

    # 'ctrl + c' exception
    except KeyboardInterrupt:
        print("\n\nExiting...\n")


if __name__ == "__main__":
    app()
