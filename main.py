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
        #Request for get IP public
        ip=requests.get("http://ifconfig.me")
        #Request for getting IP info
        geo=requests.get("http://ip-api.com/json/?fields=61439")
        #Load json
        geo=json.loads(geo.text)
        #Get uptime PC 
        uptime=subprocess.getoutput("uptime -p")
        #Get info from distro Linux
        info=platform.freedesktop_os_release()
        #Linux Like (distro)
        distro=info["ID"]
        #Init cpuinfo
        cpu=cpuinfo.get_cpu_info()
        #Shell command for getting users on your PC
        users=subprocess.getoutput("cut -d: -f1 /etc/passwd")
        #Brand exaple > Intel, AMD
        cpu_brand=cpu["brand_raw"]
        #Get IP info using ip-api.com 
        geoip=geo["country"]
        codeip=geo["countryCode"]
        isp=geo["isp"]
        return Panel(f"""[yellow]Public IP[/yellow] > [cyan]{ip.text}[/cyan]\n[yellow]Location[/yellow] > [cyan]{geoip}[/cyan] ([purple]{codeip}[/purple])
[yellow]ISP[/yellow] > [cyan]{isp}[/cyan]
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
        service=subprocess.getoutput("systemctl list-units --type=service --state=active")
        return Panel(service,title="Service")
class memory(Widget):
    def on_mount(self):
        self.set_interval(3,self.refresh)
    def render(self) -> Panel:
        """
        Trasfrom byte > K,M,G,T,P
        """
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

        #Printing
        if used < 30:
            storage=(f"[cyan]Used[/cyan] > [green]({uz} GB) {used}%[/green]\n[cyan]Free[/cyan] > [green]({fz} GB) {free}%[/green]")
        elif used > 30:
            storage=(f"[cyan]Used[/cyan] > [yellow]({uz} GB) {used}%[/yellow]\n[cyan]Free[/cyan] > [yelllow]({fz} GB) {free}[/yellow]%")
        elif used > 60:
            storage=(f"[cyan]Used[/cyan] > [red]({uz} GB) {used}%[/red]\n[cyan]Free[/cyan] > [red]({fz}) {free}[/red]")
        #init varible
        cpufreq = psutil.cpu_freq()
        partitions = psutil.disk_partitions()
        net_io = psutil.net_io_counters()
        for x in partitions:
            fstype=x.fstype
        uptime=subprocess.getoutput("uptime -p")
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
        #keymap
        await self.bind("q","quit")
    async def on_mount(self) -> None:
        #window location
        await self.view.dock(title(), edge="top", size=3)
        await self.view.dock(pie(), edge="bottom", size=3)
        #add scrolling
        scroll_view1=ScrollView(contents=memory(),auto_width=True)
        scroll_view2=ScrollView(contents=network(),auto_width=True,gutter=(1,1))
        await self.view.dock(scroll_view2, edge="right", size=30)
        await self.view.dock(scroll_view1,edge="left",size=40)
        scroll_view = ScrollView(contents=service(), auto_width=True)
        await self.view.dock(scroll_view,edge="top")
#Pinging google.com for verify internet location
url = "http://google.com"
timeout = 5
try:
	request = requests.get(url,timeout=timeout)
	Ux.run()
except (requests.ConnectionError, requests.Timeout):
	print("[red][b]No internet connection.")
