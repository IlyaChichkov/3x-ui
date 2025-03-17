import os
import sys
import os
import sys
import signal
import requests
import subprocess
import hashlib
import time

PID_FILE = "process.pid"
X_UI_PATH = "/app/x-ui/x-ui"

def show_usage():
    print(f"""
┌───────────────────────────────────────────────────────┐
│  {Colors.BLUE}x-ui control menu usages (subcommands):{Colors.PLAIN}              │
│                                                       │
│  {Colors.BLUE}x-ui{Colors.PLAIN}              - Admin Management Script          │
│  {Colors.BLUE}x-ui start{Colors.PLAIN}        - Start                            │
│  {Colors.BLUE}x-ui stop{Colors.PLAIN}         - Stop                             │
│  {Colors.BLUE}x-ui restart{Colors.PLAIN}      - Restart                          │
│  {Colors.BLUE}x-ui status{Colors.PLAIN}       - Current Status                   │
│  {Colors.BLUE}x-ui settings{Colors.PLAIN}     - Current Settings                 │
│  {Colors.BLUE}x-ui enable{Colors.PLAIN}       - Enable Autostart on OS Startup   │
│  {Colors.BLUE}x-ui disable{Colors.PLAIN}      - Disable Autostart on OS Startup  │
│  {Colors.BLUE}x-ui log{Colors.PLAIN}          - Check logs                       │
│  {Colors.BLUE}x-ui banlog{Colors.PLAIN}       - Check Fail2ban ban logs          │
│  {Colors.BLUE}x-ui update{Colors.PLAIN}       - Update                           │
│  {Colors.BLUE}x-ui legacy{Colors.PLAIN}       - legacy version                   │
│  {Colors.BLUE}x-ui install{Colors.PLAIN}      - Install                          │
│  {Colors.BLUE}x-ui uninstall{Colors.PLAIN}    - Uninstall                        │
└───────────────────────────────────────────────────────┘
""")

def print_menu():
    print(f"""
╔────────────────────────────────────────────────╗
│   {Colors.GREEN}3X-UI Panel Management Script{Colors.PLAIN}                │
│   {Colors.GREEN}0.{Colors.PLAIN} Exit Script                               │
│────────────────────────────────────────────────│
│   {Colors.GREEN}1.{Colors.PLAIN} Install                                   │
│   {Colors.GREEN}2.{Colors.PLAIN} Update                                    │
│   {Colors.GREEN}3.{Colors.PLAIN} Update Menu                               │
│   {Colors.GREEN}4.{Colors.PLAIN} Legacy Version                            │
│   {Colors.GREEN}5.{Colors.PLAIN} Uninstall                                 │
│────────────────────────────────────────────────│
│   {Colors.GREEN}6.{Colors.PLAIN} Reset Username & Password & Secret Token  │
│   {Colors.GREEN}7.{Colors.PLAIN} Reset Web Base Path                       │
│   {Colors.GREEN}8.{Colors.PLAIN} Reset Settings                            │
│   {Colors.GREEN}9.{Colors.PLAIN} Change Port                               │
│  {Colors.GREEN}10.{Colors.PLAIN} View Current Settings                     │
│────────────────────────────────────────────────│
│  {Colors.GREEN}11.{Colors.PLAIN} Start                                     │
│  {Colors.GREEN}12.{Colors.PLAIN} Stop                                      │
│  {Colors.GREEN}13.{Colors.PLAIN} Restart                                   │
│  {Colors.GREEN}14.{Colors.PLAIN} Check Status                              │
│  {Colors.GREEN}15.{Colors.PLAIN} Logs Management                           │
│────────────────────────────────────────────────│
│  {Colors.GREEN}16.{Colors.PLAIN} Enable Autostart                          │
│  {Colors.GREEN}17.{Colors.PLAIN} Disable Autostart                         │
│────────────────────────────────────────────────│
│  {Colors.GREEN}18.{Colors.PLAIN} SSL Certificate Management                │
│  {Colors.GREEN}19.{Colors.PLAIN} Cloudflare SSL Certificate                │
│  {Colors.GREEN}20.{Colors.PLAIN} IP Limit Management                       │
│  {Colors.GREEN}21.{Colors.PLAIN} Firewall Management                       │
│  {Colors.GREEN}22.{Colors.PLAIN} SSH Port Forwarding Management            │
│────────────────────────────────────────────────│
│  {Colors.GREEN}23.{Colors.PLAIN} Enable BBR                                │
│  {Colors.GREEN}24.{Colors.PLAIN} Update Geo Files                          │
│  {Colors.GREEN}25.{Colors.PLAIN} Speedtest by Ookla                        │
╚────────────────────────────────────────────────╝
""")


class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[0;33m'
    PLAIN = '\033[0m'

def download_url(url = '') -> bool:
    response = requests.get(url)
    file_name = os.path.basename(url)

    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print('File downloaded successfully')
        return True
    else:
        print('Failed to download file')
    return False


def confirm(prompt, default=None):
    if default:
        response = input(f"{prompt} [Default {default}]: ").strip()
        if not response:
            response = default
    else:
        response = input(f"{prompt} [y/n]: ").strip().lower()
    return response in ("y", "yes")

def before_show_menu():
    input(f"\n{Colors.YELLOW}Press enter to return to the main menu: {Colors.PLAIN}")
    show_menu()

def confirm_restart():
    if confirm("Restart the panel, Attention: Restarting the panel will also restart xray", "y"):
        restart()
    else:
        show_menu()

def exit():
    sys.exit(0)

def check_uninstall():
    return False

def check_install():
    return os.path.exists(X_UI_PATH)

def install(start_service = True):
    print('install')
    if download_url('https://raw.githubusercontent.com/MHSanaei/3x-ui/main/install.sh'):
        if start_service:
            start()
        else:
            start(0)
    else:
        LOGE("Failed to install, please check logs")

def update():
    pass

def update_menu():
    pass

def legacy_version():
    pass

def uninstall():
    pass

def generate_random_string(length=8):
    """Generate random string."""
    return hashlib.md5(str(time.time_ns()).encode()).hexdigest()[:length]

def reset_user():
    if not confirm("Are you sure to reset the username and password of the panel?", "n"):
        return

    config_account = input("Please set the login username [default is a random username]: ").strip()
    if not config_account:
        config_account = generate_random_string()

    config_password = input("Please set the login password [default is a random password]: ").strip()
    if not config_password:
        config_password = generate_random_string()

    result = subprocess.run([X_UI_PATH, "setting", "-username", config_account, "-password", config_password], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
            LOGE("Failed to reset username and password, please check logs")
            return

    result = subprocess.run([X_UI_PATH, "setting", "-remove_secret"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
            LOGE("Failed to remove secret, please check logs")
            return

    print(f"Panel login username has been reset to: {Colors.GREEN}{config_account}{Colors.PLAIN}")
    print(f"Panel login password has been reset to: {Colors.GREEN}{config_password}{Colors.PLAIN}")
    print(f"{Colors.YELLOW}Panel login secret token disabled{Colors.PLAIN}")
    print(f"{Colors.GREEN}Please use the new login username and password to access the X-UI panel. Also remember them!{Colors.PLAIN}")

    confirm_restart()

def reset_webbasepath():
    print(f"{Colors.YELLOW}Resetting Web Base Path{Colors.PLAIN}")

    if not confirm("Are you sure to reset the web base path?", "n"):
        return

    config_webBasePath = generate_random_string(10)
    result = subprocess.run([X_UI_PATH, "setting", "-webBasePath", config_webBasePath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        LOGE("Failed to reset web base path, please check logs")
        return

    print(f"Web base path has been reset to: {Colors.GREEN}{config_webBasePath}{Colors.PLAIN}")
    print(f"{Colors.GREEN}Please use the new web base path to access the panel.{Colors.PLAIN}")
    restart()

def reset_config():
    if confirm("Are you sure you want to reset all panel settings, "
            "Account data will not be lost, Username and password"
            " will not change", "n"):
        result = subprocess.run([X_UI_PATH, "setting", "-reset"])
        if result.returncode != 0:
            LOGE("Failed to reset config, please check logs")
            return
        print('All panel settings have been reset to default.')
        restart()

def set_port():
    port = input("Enter port number[1-65535]: ").strip()
    if not port:
        LOGD("Cancelled")
        before_show_menu()
        return
    result = subprocess.run([X_UI_PATH, "setting", "-port", port])
    if result.returncode != 0:
        LOGE("Failed to set port, please check logs")
        show_menu()
        return
    print(f"The port is set, Please restart the panel now, and use the new port {Colors.GREEN}{port}{Colors.PLAIN} to access web panel")
    confirm_restart()

def check_config():
    result = subprocess.run([X_UI_PATH, "setting", "-show", "true"], capture_output=True, text=True)
    if result.returncode != 0:
        LOGE("get current settings error, please check logs")
        show_menu()
        return
    info = result.stdout
    print(info)

def LOGE(message):
    print(f"{Colors.RED}[ERR] {message}{Colors.PLAIN}")

def check_status() -> int:
    """0 - started, 1 - not started,  2: not installed"""
    if not os.path.exists(X_UI_PATH):
        print("x-ui not installed.")
        return 2

    if not os.path.exists(PID_FILE):
        print("process isn't running.")
        return 1

    with open(PID_FILE, "r") as f:
        pid = int(f.read().strip())

    if os.path.exists(f'/proc/{pid}'):
        print(f"x-ui is running, PID: {pid}.")
        return 0
    else:
        os.remove(PID_FILE)
        return 1

def show_status():
    status = check_status()
    if status == 0:
        print(f"Panel state: {Colors.GREEN}Running{Colors.PLAIN}")
    if status == 1:
        print(f"Panel state: {Colors.YELLOW}Not Running{Colors.PLAIN}")
    if status == 2:
        print(f"Panel state: {Colors.RED}Not Installed{Colors.PLAIN}")

def update(arg=1):
    pass  # Implement update logic here

def update_menu(arg=1):
    pass  # Implement update_menu logic here

def legacy_version(arg=1):
    pass  # Implement legacy_version logic her

def start(arg=1):
    """Start x-ui process."""
    if check_status():
        process = subprocess.Popen([X_UI_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open(PID_FILE, "w") as f:
            f.write(str(process.pid))
        print(f'Start x-ui process. PID: {process.pid}')
    else:
        print('Already started!')

def stop():
    """Stop x-ui process, using file with PID."""
    if check_status():
        print("Already stopped!")
        return

    with open(PID_FILE, "r") as f:
        pid = int(f.read().strip())

    try:
        os.kill(pid, signal.SIGTERM)
        print(f"x-ui stopped.")
    except ProcessLookupError:
        print(f"x-ui process wasn't found. PID: {pid}")
    finally:
        os.remove(PID_FILE)

def restart():
    stop()
    start()

def status():
    show_status()

def show_log():
    LOGE("Not implimented yet.")

def show_banlog():
    LOGE("Not implimented yet.")

def enable():
    print("x-ui autostart enabled.")
    with open("autostart", "w") as f:
        f.write("1")

def disable():
    print("x-ui autostart disabled.")
    with open("autostart", "w") as f:
        f.write("0")

def ssl_cert_issue_main():
    LOGE("Not implimented yet.")

def ssl_cert_issue_CF():
    LOGE("Not implimented yet.")

def iplimit_main():
    LOGE("Not implimented yet.")

def firewall_menu():
    LOGE("Not implimented yet.")

def SSH_port_forwarding():
    LOGE("Not implimented yet.")

def bbr_menu():
    LOGE("Not implimented yet.")

def update_geo():
    LOGE("Not implimented yet.")

def run_speedtest():
    LOGE("Not implimented yet.")

def startup():
    print("STARTUP.")
    autostart: int = 0
    if not os.path.exists("autostart"):
        with open("autostart", 'w') as file:
            file.write("0")

    with open("autostart", "r") as f:
        autostart = int(f.read())
    if autostart:
        start()

def show_menu():
    global x_ui_commands
    run_menu = True
    
    while run_menu:
        print_menu()
        show_status()
        num = input("Please enter your selection [0-25]: ").strip()

        command_succeseded = False
        for f in x_ui_commands:
            if f['cmd'] == num:
                if callable(f['check_before']):
                    f['check_before']()
                if callable(f['function']):
                    f['function']()
                if not f['open_menu_after']:
                    run_menu = False
                command_succeseded = True

        if not command_succeseded:
            LOGE("Please enter the correct number [0-25]")

def process_cmd(arg):
    global x_ui_commands
    for f in x_ui_commands:
        if f['name'] == arg:
            if callable(f['check_before']):
                f['check_before']()
            if callable(f['function']):
                f['function']()
            return

    show_usage()

x_ui_commands = [
    {
        'cmd': '0',
        'name': 'exit',
        'function': exit,
        'check_before': None,
        'open_menu_after': True,
    },
    {
        'cmd': '1',
        'name': 'install',
        'function': install,
        'check_before': check_uninstall,
        'open_menu_after': True,
    },
    {
        'cmd': '2',
        'name': 'update',
        'function': update,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '3',
        'name': 'update_menu',
        'function': update_menu,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '4',
        'name': 'legacy_version',
        'function': legacy_version,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '5',
        'name': 'uninstall',
        'function': uninstall,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '6',
        'name': 'reset_user',
        'function': reset_user,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '7',
        'name': 'reset_webbasepath',
        'function': reset_webbasepath,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '8',
        'name': 'reset_config',
        'function': reset_config,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '9',
        'name': 'set_port',
        'function': set_port,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '10',
        'name': 'check_config',
        'function': check_config,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '11',
        'name': 'start',
        'function': start,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '12',
        'name': 'stop',
        'function': stop,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '13',
        'name': 'restart',
        'function': restart,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '14',
        'name': 'status',
        'function': status,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '15',
        'name': 'show_log',
        'function': show_log,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '16',
        'name': 'enable',
        'function': enable,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '17',
        'name': 'disable',
        'function': disable,
        'check_before': check_install,
        'open_menu_after': True,
    },
    {
        'cmd': '18',
        'name': 'ssl_cert_issue_main',
        'function': ssl_cert_issue_main,
        'check_before': None,
        'open_menu_after': True,
    },
    {
        'cmd': '19',
        'name': 'ssl_cert_issue_CF',
        'function': ssl_cert_issue_CF,
        'check_before': None,
        'open_menu_after': True,
    },
    {
        'cmd': '20',
        'name': 'iplimit_main',
        'function': iplimit_main,
        'check_before': None,
        'open_menu_after': True,
    },
    {
        'cmd': '21',
        'name': 'firewall_menu',
        'function': firewall_menu,
        'check_before': None,
        'open_menu_after': True,
    },
    {
        'cmd': '22',
        'name': 'SSH_port_forwarding',
        'function': SSH_port_forwarding,
        'check_before': None,
        'open_menu_after': True,
    },
    {
        'cmd': '23',
        'name': 'bbr_menu',
        'function': bbr_menu,
        'check_before': None,
        'open_menu_after': True,
    },
    {
        'cmd': '24',
        'name': 'update_geo',
        'function': update_geo,
        'check_before': None,
        'open_menu_after': True,
    },
    {
        'cmd': '25',
        'name': 'run_speedtest',
        'function': run_speedtest,
        'check_before': None,
        'open_menu_after': True,
    },
    {
        'cmd': '70',
        'name': 'startup',
        'function': startup,
        'check_before': None,
        'open_menu_after': False,
    },
]

if len(sys.argv) > 1:
    process_cmd(sys.argv[1])
else:
    show_menu()