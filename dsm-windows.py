#!/usr/bin/env python3
import cpuinfo
import shutil
from rich import box
import subprocess
from rich.pretty import Pretty
import time
from rich import print
import sys
from textual.views import DockView
import psutil
from rich.live import Live
from textual.app import App
from textual.widget import Widget
from textual.widgets import Placeholder,ScrollView
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
import requests
import json
from rich.progress import Progress
import platform
console=Console()

class pie(Widget):
    def render(self) -> Panel:
        return Panel("(q) [cyan]Exit")

class title(Widget):
    def render(self) -> Panel:
        return Panel(Text("Decks-Server-Manager",style="green",justify="center"),box=box.MINIMAL)

class network(Widget):
    def render(self) -> Panel:
        ip=requests.get("http://ifconfig.me")
        geo=requests.get("http://ip-api.com/json/?fields=61439")
        geo=json.loads(geo.text)
        info=platform.freedesktop_os_release()
        distro=info["ID"]
        cpu=cpuinfo.get_cpu_info()
        users=subprocess.getoutput("net users")
        cpu_brand=cpu["brand_raw"]
        geoip=geo["country"]
        codeip=geo["countryCode"]
        return Panel(f"""[yellow]Public IP[/yellow] > [cyan]{ip.text}[/cyan]\n[yellow]Location[/yellow] > [cyan]{geoip}[/cyan] ([purple]{codeip}[/purple])"
[yellow]OS[/yellow] > [cyan]{platform.system()}[/cyan]
[yellow]Distro > [/yellow][cyan]{distro}[/cyan]
[yellow]CPU[/yellow] > [cyan]{cpu_brand}[/cyan]
[yellow]---Users---[/yellow]\n[cyan]{users}[/cyan]
""",title="Network & Info")
class console(Widget):
    def on_mount(self):
        self.set_interval(1,self.refresh)
    def render(self) -> Panel:
        process=subprocess.getoutput("ps -ef")
        return Panel(process,box=box.MINIMAL,title="Process manager")
class service(Widget):
    def on_mount(self):
        self.set_interval(1,self.refresh)
    def render(self) -> Panel:
        service=subprocess.getoutput("net start")
        return Panel(service,title="Service")
class memory(Widget):
    def on_mount(self):
        self.set_interval(3,self.refresh)
    def render(self) -> Panel:
        def get_size(bytes, suffix="B"):
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor
        hdd = shutil.disk_usage('/')

        tz= hdd.total // (2**30)
        uz=hdd.used//(2**30)
        fz=hdd.free//(2**30)
        quotient = uz / tz
        used = quotient * 100
        quotient = fz / tz
        free = quotient * 100
        used=int(used)
        free=int(free)

        if used < 30:
            storage=(f"[cyan]Used[/cyan] > [green]({uz} GB) {used}%[/green]\n[cyan]Free[/cyan] > [green]({fz} GB) {free}%[/green]")
        elif used > 30:
            storage=(f"[cyan]Used[/cyan] > [yellow]({uz} GB) {used}%[/yellow]\n[cyan]Free[/cyan] > [yelllow]({fz} GB) {free}[/yellow]%")
        elif used > 60:
            storage=(f"[cyan]Used[/cyan] > [red]({uz} GB) {used}%[/red]\n[cyan]Free[/cyan] > [red]({fz}) {free}[/red]")
        cpufreq = psutil.cpu_freq()
        partitions = psutil.disk_partitions()
        net_io = psutil.net_io_counters()
        for x in partitions:
            fstype=x.fstype
        import ctypes
        lib = ctypes.windll.kernel32
        t = lib.GetTickCount64()
        t = int(str(t)[:-3])
        
        mins, sec = divmod(t, 60)
        hour, mins = divmod(mins, 60)
        days, hour = divmod(hour, 24)
        
        uptime=(f"{days} days, {hour:02}:{mins:02}:{sec:02}")
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return Panel(f"""
[red]---Disk info---[/red]
{storage}
[cyan]File System[/cyan] > [magenta]{fstype}[/magenta]
[red]---CPU Info---[/red]
[cyan]Physical cores[/cyan] > [magenta]{psutil.cpu_count(logical=False)}[/magenta]
[cyan]Cores[/cyan] > [magenta]{psutil.cpu_count(logical=True)}[/magenta]
[red]---CPU freq---[/red]
[cyan]Max freq[/cyan] > [magenta]{cpufreq.max:.2f}Mhz[/magenta]
[cyan]Min freq[/cyan] > [magenta]{cpufreq.min:.2f}Mhz[/magenta]
[cyan]Current freq[/cyan] > [magenta]{cpufreq.current:.2f}[/magenta]
[red]---CPU Usage---[/red]
[cyan]All CPU usage[/cyan] > [magenta]{psutil.cpu_percent()}%[/magenta]
[red]---Memory Monitor---[/red]
[cyan]Total[/cyan] > [magenta]{get_size(svmem.total)}[/magenta]
[cyan]Used[/cyan] > [magenta]{get_size(svmem.used)}[/magenta]
[cyan]Percentage[/cyan] > [magenta]{svmem.percent}%[/magenta]
[red]---Network Monitor---[/red]
[cyan]Total Bytes Sent[/cyan] > [magenta]{get_size(net_io.bytes_sent)}[/magenta]
[cyan]Total Bytes Received[/cyan] > [magenta]{get_size(net_io.bytes_recv)}[/magenta]
[red]---Swap---[/red]
[cyan]Total[/cyan] > [magenta]{get_size(swap.total)}[/magenta]
[cyan]Free[/cyan] > [magenta]{get_size(swap.free)}[/magenta]
[cyan]Used[/cyan] > [magenta]{get_size(swap.used)}[/magenta]
[cyan]Percentage[/cyan] > [magenta]{swap.percent}%[/magenta]
[red]---General Info---[/red]
[cyan]Uptime[/cyan] > [magenta]{uptime}[/magenta]""",title='Server status')
class Ux(App):
    async def on_load(self,event):
        await self.bind("q","quit")
    async def on_mount(self) -> None:
        await self.view.dock(title(), edge="top", size=3)
        await self.view.dock(pie(), edge="bottom", size=3)
        scroll_view1=ScrollView(contents=memory(),auto_width=True)
        scroll_view2=ScrollView(contents=network(),auto_width=True,gutter=(1,1))
        await self.view.dock(scroll_view2, edge="right", size=30)
        await self.view.dock(scroll_view1,edge="left",size=40)
        scroll_view = ScrollView(contents=service(), auto_width=True)
        await self.view.dock(scroll_view,edge="top")
url = "http://google.com"
timeout = 5
try:
	request = requests.get(url,timeout=timeout)
	Ux.run()
except (requests.ConnectionError, requests.Timeout):
	print("[red][b]No internet connection.")
