from apis import get_weather_for_city


class Assistant:
    def __init__(self, reminders, config=None):
        self.reminders = reminders
        self.config = config or {}

    def handle_command(self, text: str) -> str:
        text = text.strip()
        low = text.lower()

        if "weather" in low:
            # Example: "weather Pristina"
            parts = text.split(maxsplit=1)
            if len(parts) > 1:
                city = parts[1]
            else:
                city = self.config.get("default_city", "Pristina")
            try:
                w = get_weather_for_city(city, api_key=self.config.get("openweather_api_key"))
                return f"{w['description'].capitalize()}, {w['temp_c']:.1f}°C"
            except Exception as e:
                return f"Could not get weather: {e}"

        if low.startswith("remind") or low.startswith("set reminder"):
            created = self.reminders.add_from_text(text)
            return created

        if low.startswith("list reminders") or low == "reminders":
            items = self.reminders.list_reminders()
            if not items:
                return "No reminders set."
            lines = [f"{i+1}. {r['time']} - {r['text']}" for i, r in enumerate(items)]
            return "\n".join(lines)

        if low.startswith("help"):
            return (
                "Commands:\n"
                " - weather [city]\n"
                " - remind me at HH:MM to [task]\n"
                " - set reminder YYYY-MM-DD HH:MM [task]\n"
                " - list reminders\n"
                " - exit / quit\n"
            )

        return "I don't understand that yet. Try 'help'."
