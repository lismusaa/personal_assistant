import json
import threading
import time
from datetime import datetime
from utils.helpers import parse_reminder_text


class ReminderManager:
    def __init__(self, path: str = "data/reminders.json"):
        self.path = path
        self._lock = threading.Lock()
        self._load()

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.reminders = json.load(f)
        except FileNotFoundError:
            self.reminders = []
            self._save()

    def _save(self):
        with self._lock:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.reminders, f, ensure_ascii=False, indent=2)

    def add(self, dt: datetime, text: str) -> str:
        item = {"time": dt.isoformat(), "text": text, "notified": False}
        self.reminders.append(item)
        self._save()
        return f"Reminder set for {dt.isoformat()}: {text}"

    def add_from_text(self, raw_text: str) -> str:
        parsed = parse_reminder_text(raw_text)
        if not parsed:
            return "Could not parse reminder. Try: 'remind me at 20:00 to study'"
        dt, text = parsed
        return self.add(dt, text)

    def list_reminders(self):
        return [r for r in self.reminders if not r.get("notified")]

    def run_checker(self, poll_seconds: int = 30):
        while True:
            now = datetime.utcnow()
            changed = False
            for r in self.reminders:
                if r.get("notified"):
                    continue
                rtime = datetime.fromisoformat(r["time"])
                if rtime <= now:
                    print(f"\n[REMINDER] {r['text']} (scheduled for {r['time']})\n")
                    r["notified"] = True
                    changed = True
            if changed:
                self._save()
            time.sleep(poll_seconds)
