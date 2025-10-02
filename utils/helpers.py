from datetime import datetime, time
import re


def parse_time_hhmm(hhmm: str, date_hint: datetime = None):
    hhmm = hhmm.strip()
    m = re.match(r"^(\\d{1,2}):(\\d{2})$", hhmm)
    if not m:
        return None
    h = int(m.group(1))
    mi = int(m.group(2))
    d = date_hint.date() if date_hint else datetime.utcnow().date()
    return datetime.combine(d, time(h, mi))


def parse_reminder_text(text: str):
    text = text.strip()
    # Pattern 1: set reminder YYYY-MM-DD HH:MM <text>
    m = re.match(r"set reminder\\s+(\\d{4}-\\d{2}-\\d{2})\\s+(\\d{1,2}:\\d{2})\\s+(.+)", text, re.I)
    if m:
        date_s, time_s, rem_text = m.groups()
        try:
            dt = datetime.fromisoformat(f"{date_s}T{time_s}")
            return dt, rem_text.strip()
        except Exception:
            return None

    # Pattern 2: remind me at HH:MM to <task>
    m = re.match(r".*at\\s+(\\d{1,2}:\\d{2})\\s+to\\s+(.+)", text, re.I)
    if m:
        time_s, rem_text = m.groups()
        dt = parse_time_hhmm(time_s)
        if dt:
            return dt, rem_text.strip()

    return None
