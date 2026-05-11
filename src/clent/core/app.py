from .commands import commands
from .chat import ChatStream

messages = []

def app():
    try:
        while True:
            user_input = input("➤  ")

            if not user_input:
                continue

            # command mode
            if user_input.startswith("/") or user_input == "?":
                result = commands(user_input[1:]) if user_input.startswith("/") else commands("?")

                if result["message"]:
                    print(result["message"])

                if result["action"] == "exit":
                    break

                continue
            
            messages.append({"role": "user", "content": user_input})

            # llm mode
            print("✤  ", end="", flush=True)
            try:
                print(messages)
                full_response = ""
                for text in ChatStream(messages):
                    print(text, end="", flush=True)
                    full_response += text               
                messages.append({"role": "assistant", "content": full_response})

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

