
import threading
import json
from assistant import Assistant
from reminders import ReminderManager

CONFIG_PATH = "data/config.json"


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("config.json not found in data/. Create it from the template.")
        return {}


def main():
    config = load_config()

    # Create assistant & reminder manager
    reminders = ReminderManager("data/reminders.json")
    assistant = Assistant(reminders=reminders, config=config)

    # Start background reminder checker thread
    reminder_thread = threading.Thread(target=reminders.run_checker, daemon=True)
    reminder_thread.start()

    print("Personal Assistant (CLI) — type 'help' for commands, 'exit' to quit")
    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if user_input.strip().lower() in ("exit", "quit"):
            print("Exiting...")
            break
        if not user_input.strip():
            continue

        response = assistant.handle_command(user_input)
        print("Assistant:", response)


if __name__ == "__main__":
    main()
