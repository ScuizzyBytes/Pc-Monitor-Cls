import requests

import time

class DiscordNotifier:
    def __init__(self, webhook_url: str, threshold: float = 85.0, cooldown_seconds: int = 60):
        self.webhook_url = webhook_url
        self.threshold = threshold
        self.cooldown_seconds = cooldown_seconds
        self.last_alert_time = 0

    def check_and_send(self, cpu_percent: float, ram_percent: float):
        current_time = time.time()

        if (cpu_percent >= self.threshold or ram_percent >= self.threshold):
            if current_time - self.last_alert_time > self.cooldown_seconds:
                self._send_embed(cpu_percent, ram_percent)
                self.last_alert_time = current_time

    def _send_embed(self, cpu_percent: float, ram_percent: float):
        embed = {
            "title": "🚨 SYSTEM WARNING: High Resource Usage",
            "color": 15158332,
            "fields": [
                {"name": "⚙️ CPU Load", "value": f"**{cpu_percent}%**", "inline": True},
                {"name": "🧠 RAM Usage", "value": f"**{ram_percent}%**", "inline": True},
            ],
            "footer": {"text": "PC Monitoring Daemon • Alert Triggered"}
        }

        payload = {"username": "System Sentinel", "embeds": [embed]}

        try:
            requests.post(self.webhook_url, json=payload, timeout=5)
        except Exception as e:
            pass