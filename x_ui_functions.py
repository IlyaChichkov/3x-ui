import os
import sys
import requests
import subprocess

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

def install():
    pass

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
    pass

def set_port():
    port = input("Enter port number[1-65535]: ").strip()
    if not port:
        LOGD("Cancelled")
        before_show_menu()
        return
    subprocess.run(["/usr/local/x-ui/x-ui", "setting", "-port", port])
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
