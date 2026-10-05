import logging
import time

from monitor import SystemMonitor
from notifier import DiscordNotifier
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1556719329024675942/t3BEKcR0jpELX3w9Mv_cGCqhUFjzXBWxzP8vF-hdHivtAfF7R37EPgQ2z1cuhaHkGqN1"    

def make_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )

    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    return layout

def generate_metrics_panel(monitor: SystemMonitor):
    cpu = monitor.cpu_info()
    ram = monitor.get_ram_info()
    disk = monitor.get_disk_info()

    table = Table.grid(expand=True)
    table.add_column()

    table.add_row(f"[bold cyan]CPU: Load[/bold cyan] {cpu['overall']}%")
    table.add_row(f"[bold green]RAM: Usage[/bold green] {ram['percent']}% {ram['used_gb']} / {ram['total_gb']} GB")
    table.add_row(f"[bold yellow]DISK: Space[/bold yellow] {disk['percent']}% {disk['used_gb']} / {disk['total_gb']} GB")

    return Panel(table, title="[bold] System Status[/bold]", border_style="bright_blue")

def generatoe_process_panel(monitor: SystemMonitor) -> Panel:
    top_procs = monitor.get_top_processes()

    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("PID", style="dim", width=6)
    table.add_column("Name")
    table.add_column("RAM %", justify="right")

    for proc in top_procs:
        ram_p = round(proc['memory_percent'] or 0, 1)
        table.add_row(str(proc['pid']), str(proc['name']), f"{ram_p}%")

    return Panel(table, title="[bold]Top RAM Processes[/bold]", border_style="magenta")

def main():
    monitor = SystemMonitor()
    notifier = DiscordNotifier(webhook_url=DISCORD_WEBHOOK_URL, threshold=85.0)
    layout = make_layout()

    layout["header"].update(Panel("[bold white center]🖥️ PYTHON CLI SYSTEM MONITORING DASHBOARD[/bold white center]", style="on blue"))
    layout["footer"].update(Panel("[dim center]Press Ctrl+C to exit • Auto Refresh every1 1s[/dim center]"))

    with Live(layout, refresh_per_second=1, screen=True):
        try:
            while True:
                layout["left"].update(generate_metrics_panel(monitor))
                layout["right"].update(generatoe_process_panel(monitor))

                if DISCORD_WEBHOOK_URL:
                    try:
                        cpu_info = monitor.cpu_info()
                        ram_info = monitor.get_ram_info()
                        notifier.check_and_send(cpu_info['overall'], ram_info['percent'])
                    except Exception:
                        pass

                    time.sleep(1)
        except KeyboardInterrupt:
            pass
        
main()