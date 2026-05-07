#!/usr/bin/env python3
import os
import re
import sys
import socket
import ipaddress
import threading
import requests
import concurrent.futures
import time
from datetime import datetime

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, MofNCompleteColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from colorama import init
from urllib3.exceptions import InsecureRequestWarning
import warnings

# ============ SETUP ============
init(autoreset=True)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()

console = Console()
lock = threading.Lock()

# Termux/Android path setup for clean output separation
BASE_DIR = "/storage/emulated/0/Download/DarkX_Results"
os.makedirs(BASE_DIR, exist_ok=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ============ MAIN UI BANNER ============
def banner():
    clear_screen()
    logo = """[bold red]
██████╗  █████╗ ██████╗ ██╗  ██╗██╗  ██╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝╚██╗██╔╝
██║  ██║███████║██████╔╝█████╔╝  ╚███╔╝ 
██║  ██║██╔══██║██╔══██╗██╔═██╗  ██╔██╗ 
██████╔╝██║  ██║██║  ██║██║  ██╗██╔╝ ██╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
             N E T W O R K
[/bold red]"""
    console.print(Align.center(logo))
    
    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column(style="bold red", justify="right")
    info_table.add_column(style="white")
    
    # User requested edits applied here (v3.0 -> v1.0 and added Developer Ashif)
    info_table.add_row("System:", "DarkXNetwork Advanced Arsenal v1.0")
    info_table.add_row("Developer:", "Ashif")
    info_table.add_row("Status:", "[green]Online & Secured[/green]")
    info_table.add_row("Filter:", "[yellow]Anti-Redirect Engine Active[/yellow]")
    
    console.print(Panel(Align.center(info_table), border_style="cyan", padding=(0, 1)))

def make_out(name):
    path = os.path.join(BASE_DIR, name)
    os.makedirs(path, exist_ok=True)
    return path

def refresh_tool():
    console.print("\n[bold cyan]↻ Re-initializing interface...[/bold cyan]")
    time.sleep(1)
    return

# ============ MODULES with embedded Jio/302 filtering ============
def host_scanner():
    banner()
    console.print("[bold cyan]❖ MODULE: Advanced Host Scanner[/bold cyan]\n")
    infile = console.input("[cyan]↳ Enter target domain list: [/cyan]").strip()
    if not os.path.exists(infile): console.print("[bold red]⨯ File not located![/bold red]"); time.sleep(1); return
    outdir = make_out(console.input("[cyan]↳ Output folder name: [/cyan]").strip() or "Host_Scanner")
    ports_input = console.input("[cyan]↳ Target ports (comma separated) [80,443,8080]: [/cyan]").strip()
    ports = [p.strip() for p in ports_input.split(",")] if ports_input else ["80", "443", "8080"]
    try: threads = int(console.input("[cyan]↳ Max threads [80]: [/cyan]").strip() or 80)
    except: threads = 80
    method = {"1":"GET", "2":"HEAD", "3":"POST", "4":"PUT"}.get(console.input("[cyan]↳ HTTP Method (1:GET, 2:HEAD) [1]: [/cyan]").strip() or "1", "GET")
    
    try:
        with open(infile, 'r') as f: domains = [line.strip() for line in f if line.strip()]
    except: console.print("[bold red]⨯ Read error![/bold red]"); time.sleep(1); return
    
    total = len(domains) * len(ports)
    res_file, ip_file = os.path.join(outdir, "results.txt"), os.path.join(outdir, "ips.txt")
    open(res_file, 'w').close(); open(ip_file, 'w').close()
    
    console.print(f"\n[bold green]✔ Engine engaged: {len(domains)} targets | Ports: {ports}[/bold green]\n")
    
    def scan_host(domain, port, progress, task_id):
        try:
            url = f"https://{domain}" if port == "443" else f"http://{domain}:{port}"
            try: ip = socket.gethostbyname(domain)
            except: ip = "N/A"
            req = getattr(requests, method.lower())
            resp = req(url, timeout=3, verify=False, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=False)
            status, server = resp.status_code, resp.headers.get("Server", "Unknown")
            
            # CORE SC SCANNER FEATURE: Jio/302 Redirect Filtering
            if status == 302 and any(x in resp.headers.get("Location", "").lower() for x in ["jio.com", "airtel", "captive"]): return
            if status in [301, 302, 303, 307, 308] and any(x in resp.text.lower() for x in ["jio", "airtel", "captive"]): return
            
            with lock:
                console.print(f"[cyan][{status}][/cyan] [yellow]{ip}[/yellow] ┋ [white]{domain}:{port}[/white] ┋ [green]{server[:15]}[/green]")
                with open(res_file, "a") as f: f.write(f"{status} | {server} | {ip} | {domain}:{port}\n")
                if ip != "N/A":
                    with open(ip_file, "a") as ipf: ipf.write(ip + "\n")
        except: pass
        finally: progress.update(task_id, advance=1)
    
    with Progress(SpinnerColumn(style="cyan"), TaskProgressColumn(), BarColumn(style="cyan"), MofNCompleteColumn(), TimeRemainingColumn(), console=console) as p:
        task = p.add_task("[cyan]Injecting payloads...", total=total)
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
            [ex.submit(scan_host, d, pt, p, task) for d in domains for pt in ports]
            
    input("\n[Press Enter to return to Command Center]")

def cidr_scanner():
    banner()
    console.print("[bold cyan]❖ MODULE: CIDR Network Mapper[/bold cyan]\n")
    try: net = ipaddress.ip_network(console.input("[cyan]↳ Enter CIDR (e.g., 192.168.1.0/24): [/cyan]").strip(), strict=False)
    except: console.print("[bold red]⨯ Invalid format![/bold red]"); time.sleep(1); return
    outdir = make_out(console.input("[cyan]↳ Output folder name: [/cyan]").strip() or "CIDR_Scanner")
    ports_input = console.input("[cyan]↳ Target ports [80,443]: [/cyan]").strip()
    ports = [p.strip() for p in ports_input.split(",")] if ports_input else ["80", "443"]
    try: threads = int(console.input("[cyan]↳ Max threads [150]: [/cyan]").strip() or 150)
    except: threads = 150
    hosts = [str(ip) for ip in net.hosts()]
    res_file = os.path.join(outdir, "results.txt"); open(res_file, 'w').close()
    
    console.print(f"\n[bold green]✔ Mapping {len(hosts)} IPs...[/bold green]\n")
    def scan_ip(ip, port, progress, task_id):
        try:
            resp = requests.get(f"http://{ip}:{port}", timeout=2, verify=False, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=False)
            status, server = resp.status_code, resp.headers.get('Server', 'Unknown')
            
            # SC SCANNER FEATURE: Jio/Captive Filtering
            if status == 302 and any(x in resp.headers.get("Location", "").lower() for x in ["jio", "airtel", "captive"]): return
            with lock:
                console.print(f"[cyan][{status}][/cyan] [yellow]{ip}:{port}[/yellow] ┋ [green]{server[:20]}[/green]")
                with open(res_file, "a") as f: f.write(f"{status} | {server} | {ip}:{port}\n")
        except: pass
        finally: progress.update(task_id, advance=1)
    
    with Progress(SpinnerColumn(style="cyan"), TaskProgressColumn(), BarColumn(style="cyan"), MofNCompleteColumn(), TimeRemainingColumn(), console=console) as p:
        task = p.add_task("[cyan]Scanning blocks...", total=len(hosts)*len(ports))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
            [ex.submit(scan_ip, ip, pt, p, task) for ip in hosts for pt in ports]
    input("\n[Press Enter to return to Command Center]")

def domain_extractor():
    banner()
    console.print("[bold cyan]❖ MODULE: Spider Domain Extractor[/bold cyan]\n")
    outdir = make_out(console.input("[cyan]↳ Output folder name: [/cyan]").strip() or "Domain_Extractor")
    choice = console.input("[cyan]↳ Source (1: Paste Text, 2: Load File): [/cyan]").strip()
    text = ""
    if choice == "1":
        console.print("\n[bold yellow][*] Paste payload (Press Enter TWICE to execute):[/bold yellow]")
        lines, blank = [], 0
        while True:
            line = input()
            if not line.strip():
                blank += 1
                if blank == 2: break
            else: blank = 0; lines.append(line)
        text = "\n".join(lines)
    elif choice == "2":
        try:
            with open(console.input("[cyan]↳ File path: [/cyan]").strip(), 'r', errors='ignore') as f: text = f.read()
        except: console.print("[bold red]⨯ Load failed![/bold red]"); time.sleep(1); return
    domain_pattern = re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b')
    domains = set(domain_pattern.findall(text))
    filtered = sorted({d.lower() for d in domains if len(d) > 4 and not d.startswith("www.") and not d.endswith(".com.com")})
    with open(os.path.join(outdir, "domains.txt"), 'w') as f:
        for d in filtered: f.write(d + "\n")
    console.print(f"\n[bold green]✔ Harvested {len(filtered)} valid domains.[/bold green]")
    input("\n[Press Enter to return to Command Center]")

def multi_cidr():
    banner()
    console.print("[bold cyan]❖ MODULE: Multi-CIDR Recon[/bold cyan]\n")
    infile = console.input("[cyan]↳ CIDR list file: [/cyan]").strip()
    if not os.path.exists(infile): console.print("[red]⨯ Missing![/red]"); time.sleep(1); return
    outdir = make_out(console.input("[cyan]↳ Output folder: [/cyan]").strip() or "Multi_CIDR")
    port = console.input("[cyan]↳ Target port [80]: [/cyan]").strip() or "80"
    try: threads = int(console.input("[cyan]↳ Threads [200]: [/cyan]").strip() or 200)
    except: threads = 200
    with open(infile, 'r') as f: cidrs = [l.strip() for l in f if l.strip()]
    ips = []
    for c in cidrs:
        try: ips.extend([str(i) for i in ipaddress.ip_network(c, strict=False).hosts()])
        except: pass
    res_file = os.path.join(outdir, "results.txt"); open(res_file, 'w').close()
    
    def scan_ip(ip, port, p, task):
        try:
            resp = requests.get(f"http://{ip}:{port}", timeout=2, verify=False, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=False)
            # Core Redirect Filtering retained
            if resp.status_code == 302 and any(x in resp.headers.get("Location", "").lower() for x in ["jio", "airtel", "captive"]): return
            with lock:
                console.print(f"[cyan][{resp.status_code}][/cyan] [yellow]{ip}:{port}[/yellow]")
                with open(res_file, "a") as f: f.write(f"{resp.status_code} | {ip}:{port}\n")
        except: pass
        finally: p.update(task, advance=1)

    with Progress(SpinnerColumn(style="cyan"), TaskProgressColumn(), BarColumn(style="cyan"), MofNCompleteColumn(), TimeRemainingColumn(), console=console) as p:
        task = p.add_task("[cyan]Mapping networks...", total=len(ips))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
            [ex.submit(scan_ip, ip, port, p, task) for ip in ips]
    input("\n[Press Enter to return to Command Center]")

def multi_port():
    banner()
    console.print("[bold cyan]❖ MODULE: Deep Port Scanner[/bold cyan]\n")
    domain = console.input("[cyan]↳ Target Domain/IP: [/cyan]").strip()
    p_in = console.input("[cyan]↳ Ports (comma separated) [Default Common]: [/cyan]").strip()
    
    ports = []
    if p_in: ports = [int(p.strip()) for p in p_in.split(",")]
    else: ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389]
        
    try: ip_addr = socket.gethostbyname(domain)
    except: ip_addr = domain
    
    console.print(f"\n[bold green]Probing {ip_addr}...[/bold green]\n")
    
    def scan_port(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1)
            res = s.connect_ex((ip_addr, port)); s.close()
            return port, res == 0
        except: return port, False

    with Progress(SpinnerColumn(style="cyan"), TaskProgressColumn(), BarColumn(style="cyan"), MofNCompleteColumn(), TimeRemainingColumn(), console=console) as p:
        task = p.add_task("[cyan]Probing ports...", total=len(ports))
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
            futs = {ex.submit(scan_port, pt): pt for pt in ports}
            for fut in concurrent.futures.as_completed(futs):
                pt, is_open = fut.result()
                if is_open: console.print(f"[bold green]✔ Port {pt} is OPEN[/bold green]")
                p.update(task, advance=1)
    input("\n[Press Enter to return to Command Center]")

def subdomain_hunt():
    banner()
    console.print("[bold cyan]❖ MODULE: Subdomain Hunter[/bold cyan]\n")
    domain = console.input("[cyan]↳ Root Domain (example.com): [/cyan]").strip()
    subs = ["www", "mail", "ftp", "admin", "api", "blog", "cdn", "dev", "test", "staging", "portal"]
    found = []
    def check_sub(sub):
        try: socket.gethostbyname(f"{sub}.{domain}"); return f"{sub}.{domain}"
        except: return None
    with Progress(SpinnerColumn(style="cyan"), TaskProgressColumn(), BarColumn(style="cyan"), MofNCompleteColumn(), TimeRemainingColumn(), console=console) as p:
        task = p.add_task("[cyan]Brute-forcing DNS...", total=len(subs))
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
            futs = {ex.submit(check_sub, s): s for s in subs}
            for fut in concurrent.futures.as_completed(futs):
                if res := fut.result():
                    console.print(f"[bold green]✔ Hit:[/bold green] [white]{res}[/white]"); found.append(res)
                p.update(task, advance=1)
    input("\n[Press Enter to return to Command Center]")

def split_txt():
    banner()
    console.print("[bold cyan]❖ MODULE: Payload Splitter[/bold cyan]\n")
    infile = console.input("[cyan]↳ Target file: [/cyan]").strip()
    if not os.path.exists(infile): console.print("[red]⨯ Not found![/red]"); time.sleep(1); return
    lines_per = int(console.input("[cyan]↳ Lines per chunk [1000]: [/cyan]").strip() or 1000)
    outdir = make_out("File_Splitter")
    with open(infile, 'r', errors='ignore') as f: lines = f.readlines()
    num = (len(lines) + lines_per - 1) // lines_per
    for i in range(num):
        with open(os.path.join(outdir, f"chunk_{i+1}.txt"), 'w') as f:
            f.writelines(lines[i * lines_per : (i+1) * lines_per])
    console.print(f"\n[bold green]✔ Splintered into {num} blocks.[/bold green]")
    input("\n[Press Enter to return to Command Center]")

def cidr_to_domain():
    banner()
    console.print("[bold cyan]❖ MODULE: Reverse DNS Mapper[/bold cyan]\n")
    try: cidr = ipaddress.ip_network(console.input("[cyan]↳ Enter CIDR: [/cyan]").strip(), strict=False)
    except: console.print("[red]⨯ Invalid syntax![/red]"); time.sleep(1); return
    hosts = list(cidr.hosts())
    def rev_lookup(ip, p, task):
        try:
            name = socket.gethostbyaddr(str(ip))[0]
            with lock: console.print(f"[cyan]{ip}[/cyan] ┋ [green]{name}[/green]")
        except: pass
        finally: p.update(task, advance=1)
    with Progress(SpinnerColumn(style="cyan"), TaskProgressColumn(), BarColumn(style="cyan"), MofNCompleteColumn(), TimeRemainingColumn(), console=console) as p:
        task = p.add_task("[cyan]Resolving...", total=len(hosts))
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
            [ex.submit(rev_lookup, ip, p, task) for ip in hosts]
    input("\n[Press Enter to return to Command Center]")

def remove_domain():
    banner()
    console.print("[bold cyan]❖ MODULE: List Sanitizer[/bold cyan]\n")
    infile = console.input("[cyan]↳ Target file: [/cyan]").strip()
    if not os.path.exists(infile): console.print("[red]⨯ Not found![/red]"); time.sleep(1); return
    with open(infile, 'r', errors='ignore') as f: domains = [l.strip().lower() for l in f if l.strip()]
    uniq = sorted(set(domains))
    outdir = make_out("Sanitized_Lists")
    with open(os.path.join(outdir, "clean_list.txt"), 'w') as f:
        for d in uniq: f.write(d + "\n")
    console.print(f"\n[bold green]✔ Original: {len(domains)} | Preserved: {len(uniq)}[/bold green]")
    input("\n[Press Enter to return to Command Center]")

def host_info():
    banner()
    console.print("[bold cyan]❖ MODULE: Node Interrogation[/bold cyan]\n")
    domain = console.input("[cyan]↳ Target Domain/IP: [/cyan]").strip()
    try: console.print(f"\n[bold green]✔ Resolved IP:[/bold green] [white]{socket.gethostbyname(domain)}[/white]")
    except: console.print("[red]⨯ Resolution failed.[/red]")
    input("\n[Press Enter to return to Command Center]")

def dev_info():
    banner()
    console.print(Panel(
        "[bold cyan]DARKXNETWORK ARSENAL[/bold cyan]\n\n"
        "[white]Architect:[/white] @DarkXNetwork\n"
        "[white]Version:[/white] 1.0.0-STABLE\n"
        "[white]Developer:[/white] Ashif\n"
        "[red]Warning: Unauthorized distribution is strictly monitored.[/red]",
        border_style="red"
    ))
    input("\n[Press Enter to return to Command Center]")

# ============ MAIN MENU ============
def main():
    while True:
        banner()
        
        # Single-Column Termux-Friendly UI (screens image_7 look)
        console.print("[bold white] ╭───[ CORE EXECUTABLES ]─────────────────────────╮[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]01[/bold cyan] [bold red]━[/bold red] [white]Advanced Host Scanner[/white]                    [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]02[/bold cyan] [bold red]━[/bold red] [white]CIDR Network Mapper[/white]                      [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]03[/bold cyan] [bold red]━[/bold red] [white]Spider Domain Extractor[/white]                  [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]04[/bold cyan] [bold red]━[/bold red] [white]Multi-CIDR Recon[/white]                         [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]05[/bold cyan] [bold red]━[/bold red] [white]Deep Port Scanner[/white]                        [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]06[/bold cyan] [bold red]━[/bold red] [white]Subdomain Hunter[/white]                         [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]07[/bold cyan] [bold red]━[/bold red] [white]Payload Splitter[/white]                         [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]08[/bold cyan] [bold red]━[/bold red] [white]Reverse DNS Mapper[/white]                       [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]09[/bold cyan] [bold red]━[/bold red] [white]List Sanitizer[/white]                           [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]10[/bold cyan] [bold red]━[/bold red] [white]Node Interrogation[/white]                       [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold cyan]11[/bold cyan] [bold red]━[/bold red] [white]System Information / Dev[/white]                 [bold white]│[/bold white]")
        console.print("[bold white] │[/bold white] [bold red]00[/bold red] [bold red]━[/bold red] [bold red]Terminate Session[/bold red]                        [bold white]│[/bold white]")
        console.print("[bold white] ╰────────────────────────────────────────────────╯[/bold white]")
        
        # Display output path clearly
        console.print(f"[dim]Output Path: {BASE_DIR}[/dim]")
        
        choice = console.input("\n[bold yellow]DarkX@Root:~# [/bold yellow]").strip()
        
        options = {
            "01": host_scanner, "1": host_scanner,
            "02": cidr_scanner, "2": cidr_scanner,
            "03": domain_extractor, "3": domain_extractor,
            "04": multi_cidr, "4": multi_cidr,
            "05": multi_port, "5": multi_port,
            "06": subdomain_hunt, "6": subdomain_hunt,
            "07": split_txt, "7": split_txt,
            "08": cidr_to_domain, "8": cidr_to_domain,
            "09": remove_domain, "9": remove_domain,
            "10": host_info, "11": dev_info
        }
        
        if choice in ["00", "0"]:
            console.print("\n[bold red]☠ Terminating secure connection... Logging off.[/bold red]")
            break
        elif choice in options:
            try: options[choice]()
            except KeyboardInterrupt:
                console.print("\n[red]⨯ Operation aborted by user.[/red]")
                time.sleep(1)
        else:
            console.print("[red]⨯ Unrecognized syntax. Try 01-11 or 00 to exit.[/red]")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]System halt. Terminating connection...[/bold red]")
