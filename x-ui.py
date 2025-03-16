import os
import sys
import os
import sys
import requests
import subprocess

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
    return True

def check_config():
    result = subprocess.run(["/usr/local/x-ui/x-ui", "setting", "-show", "true"], capture_output=True, text=True)
    if result.returncode != 0:
        LOGE("get current settings error, please check logs")
        show_menu()
        return
    info = result.stdout
    print(info)

def install(start_service = True):
    result = subprocess.run(["bash", "-c", "curl -Ls https://raw.githubusercontent.com/IlyaChichkov/3x-ui/main/install.sh"], shell=True)
    if result.returncode == 0:
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

def reset_user():
    pass

def reset_webbasepath():
    pass

def reset_config():
    if confirm("Are you sure you want to reset all panel settings, "
            "Account data will not be lost, Username and password"
            " will not change", "n"):
        result = subprocess.run(["/usr/local/x-ui/x-ui", "setting", "-reset"])
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
    result = subprocess.run(["/usr/local/x-ui/x-ui", "setting", "-port", port])
    if result.returncode != 0:
        LOGE("Failed to set port, please check logs")
        show_menu()
        return
    print(f"The port is set, Please restart the panel now, and use the new port {Colors.GREEN}{port}{Colors.PLAIN} to access web panel")
    confirm_restart()

def start():
    pass

def stop():
    pass

def restart():
    pass

def status():
    pass

def show_log():
    pass

def enable():
    pass

def disable():
    pass

def ssl_cert_issue_main():
    pass

def ssl_cert_issue_CF():
    pass

def iplimit_main():
    pass

def firewall_menu():
    pass

def SSH_port_forwarding():
    pass

def bbr_menu():
    pass

def update_geo():
    pass

def run_speedtest():
    pass

def LOGE(message):
    print(f"{Colors.RED}[ERR] {message}{Colors.PLAIN}")

class Application():
    def __init__(self):
        self.process = None
        self.is_running = False

app = Application()

def check_status():
    if app.is_running:
        return 0
    else:
        return 1

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[0;33m'
    PLAIN = '\033[0m'

def show_status():
    status = check_status()
    if status == 0:
        print(f"Panel state: {Colors.GREEN}Running{Colors.PLAIN}")
    if status == 1:
        print(f"Panel state: {Colors.YELLOW}Not Running{Colors.PLAIN}")
    if status == 2:
        print(f"Panel state: {Colors.RED}Not Installed{Colors.PLAIN}")

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

def show_menu():
    run_menu = True
    
    while run_menu:
        print_menu()
        show_status()
        num = input("Please enter your selection [0-25]: ").strip()

        functions = [
            {
                'cmd': '0',
                'function': exit,
                'check_before': None
            },
            {
                'cmd': '1',
                'function': install,
                'check_before': check_uninstall
            },
            {
                'cmd': '2',
                'function': update,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '3',
                'function': update_menu,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '4',
                'function': legacy_version,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '5',
                'function': uninstall,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '6',
                'function': reset_user,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '7',
                'function': reset_webbasepath,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '8',
                'function': reset_config,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '9',
                'function': set_port,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '10',
                'function': check_config,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '11',
                'function': start,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '12',
                'function': stop,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '13',
                'function': restart,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '14',
                'function': status,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '15',
                'function': show_log,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '16',
                'function': enable,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '17',
                'function': disable,
                'check_before': check_install,
                'open_menu_after': True,
            },
            {
                'cmd': '18',
                'function': ssl_cert_issue_main,
                'check_before': None,
                'open_menu_after': True,
            },
            {
                'cmd': '19',
                'function': ssl_cert_issue_CF,
                'check_before': None,
                'open_menu_after': True,
            },
            {
                'cmd': '20',
                'function': iplimit_main,
                'check_before': None,
                'open_menu_after': True,
            },
            {
                'cmd': '21',
                'function': firewall_menu,
                'check_before': None,
                'open_menu_after': True,
            },
            {
                'cmd': '22',
                'function': SSH_port_forwarding,
                'check_before': None,
                'open_menu_after': True,
            },
            {
                'cmd': '23',
                'function': bbr_menu,
                'check_before': None,
                'open_menu_after': True,
            },
            {
                'cmd': '24',
                'function': update_geo,
                'check_before': None,
                'open_menu_after': True,
            },
            {
                'cmd': '25',
                'function': run_speedtest,
                'check_before': None,
                'open_menu_after': True,
            },
        ]

        command_succeseded = False
        for f in functions:
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

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == "start":
        check_install(0) and start(0)
    elif arg == "stop":
        check_install(0) and stop(0)
    elif arg == "restart":
        check_install(0) and restart(0)
    elif arg == "status":
        check_install(0) and status(0)
    elif arg == "settings":
        check_install(0) and check_config(0)
    elif arg == "enable":
        check_install(0) and enable(0)
    elif arg == "disable":
        check_install(0) and disable(0)
    elif arg == "log":
        check_install(0) and show_log(0)
    elif arg == "banlog":
        check_install(0) and show_banlog(0)
    elif arg == "update":
        check_install(0) and update(0)
    elif arg == "legacy":
        check_install(0) and legacy_version(0)
    elif arg == "install":
        check_uninstall(0) and install(0)
    elif arg == "uninstall":
        check_install(0) and uninstall(0)
    else:
        show_usage()
else:
    show_menu()

class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    PLAIN = '\033[0m'

def check_install(arg=1):
    pass  # Implement check_install logic here

def check_uninstall(arg=1):
    pass  # Implement check_uninstall logic here

def install(arg=1):
    pass  # Implement install logic here

def update(arg=1):
    pass  # Implement update logic here

def update_menu(arg=1):
    pass  # Implement update_menu logic here

def legacy_version(arg=1):
    pass  # Implement legacy_version logic here

def uninstall(arg=1):
    pass  # Implement uninstall logic here

def reset_user(arg=1):
    pass  # Implement reset_user logic here

def reset_webbasepath(arg=1):
    pass  # Implement reset_webbasepath logic here

def reset_config(arg=1):
    pass  # Implement reset_config logic here

def set_port(arg=1):
    pass  # Implement set_port logic here

def check_config(arg=1):
    pass  # Implement check_config logic here

def start(arg=1):
    pass  # Implement start logic here

def stop(arg=1):
    pass  # Implement stop logic here

def restart(arg=1):
    pass  # Implement restart logic here

def status(arg=1):
    pass  # Implement status logic here

def show_log(arg=1):
    pass  # Implement show_log logic here

def show_banlog(arg=1):
    pass  # Implement show_banlog logic here

def enable(arg=1):
    pass  # Implement enable logic here

def disable(arg=1):
    pass  # Implement disable logic here

def ssl_cert_issue_main():
    pass  # Implement ssl_cert_issue_main logic here

def ssl_cert_issue_CF():
    pass  # Implement ssl_cert_issue_CF logic here

def iplimit_main():
    pass  # Implement iplimit_main logic here

def firewall_menu():
    pass  # Implement firewall_menu logic here

def SSH_port_forwarding():
    pass  # Implement SSH_port_forwarding logic here

def bbr_menu():
    pass  # Implement bbr_menu logic here

def update_geo():
    pass  # Implement update_geo logic here

def run_speedtest():
    pass  # Implement run_speedtest logic here

def show_status():
    pass  # Implement show_status logic here
