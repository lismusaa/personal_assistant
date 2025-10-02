import threading
import tkinter as tk
from assistant import Assistant
from reminders import ReminderManager


class SimpleGUI:
    def __init__(self, root, config=None):
        self.root = root
        self.root.title("Personal Assistant")
        self.config = config or {}

        self.reminders = ReminderManager("data/reminders.json")
        self.assistant = Assistant(reminders=self.reminders, config=self.config)

        self.text = tk.Text(root, height=15, width=60)
        self.text.pack()

        self.entry = tk.Entry(root, width=60)
        self.entry.pack()
        self.entry.bind('<Return>', self.on_enter)

    def on_enter(self, event=None):
        user = self.entry.get()
        self.entry.delete(0, 'end')
        resp = self.assistant.handle_command(user)
        self.text.insert('end', f"You: {user}\nAssistant: {resp}\n\n")
        self.text.see('end')


def run_gui(config=None):
    root = tk.Tk()
    app = SimpleGUI(root, config=config)
    t = threading.Thread(target=app.reminders.run_checker, daemon=True)
    t.start()
    root.mainloop()
