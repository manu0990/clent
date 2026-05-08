from .commands import commands


def app():
    try:
        while True:
            user_input = input("➤ ").strip()

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

            # llm mode
            print(f"✤ {user_input}\n")

    # 'ctrl + c' exception
    except KeyboardInterrupt:
        print("\n\nExiting...\n")


if __name__ == "__main__":
    app()