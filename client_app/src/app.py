import os
import platform
import time
import subprocess
import re
import socket
import psutil
import requests
import winreg

# Constants
# API_URL = "https://eoet8zb67t6tna5.m.pipedream.net"
API_URL = "https://localhost:44359/Receiver.aspx"
HEADERS = {'Content-Type': 'application/json'}
INTERVAL = 1  # Run every 1 seconds for efficiency and lower server load

# Utility Functions
def run_command(command, decode=True):
    """Runs a shell command and returns the output."""
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode() if decode else output
    except subprocess.CalledProcessError as e:
        log_error(f"Command failed: {command}. Error: {str(e)}")
        return None

def log_error(message):
    """Logs error messages to a file."""
    with open('error.log', 'a') as f:
        f.write(f"{time.ctime()}: {message}\n")

# System Information
def get_system_info():
    """Collects system information of the device."""
    return {
        'system': f"{platform.system()} {platform.release()}",
        'version': platform.version(),
        'processor': get_formatted_processor(),
        'total_ram': get_total_ram()
    }

def get_formatted_processor():
    """Fetches and formats the processor information."""
    os_name = platform.system()
    commands = {
        "Windows": ['wmic', 'cpu', 'get', 'name'],
        "Linux": ['lscpu'],
        "Darwin": ['sysctl', '-n', 'machdep.cpu.brand_string']
    }
    
    output = run_command(commands.get(os_name))
    if not output:
        return platform.processor()  # Fallback if command fails
    
    return extract_processor_name(output, os_name)

def extract_processor_name(output, os_name):
    """Extracts processor name based on OS."""
    os_extractors = {
        "Windows": lambda x: x.split('\n')[1].strip(),
        "Linux": lambda x: re.search(r'Model name:\s*(.*)', x).group(1).strip(),
        "Darwin": lambda x: x.strip()
    }
    return os_extractors[os_name](output) + f" {get_system_type()}"

def get_total_ram():
    """Fetches the total RAM of the device in GB."""
    total_memory = psutil.virtual_memory().total
    return round(total_memory / (1024 ** 3), 2)

def get_system_type():
    """Fetches the system type (e.g., 64-bit)."""
    return "64-bit" if platform.machine().endswith('64') else "32-bit"

# Network Information
def get_network_info():
    """Collects network information of the device."""
    return {
        'mac_address': get_mac_address(),
        'ip_address': get_ip_address(),
        'domain_info': get_domain_info()
    }

def get_mac_address():
    """Fetches the MAC address of the device."""
    interfaces = psutil.net_if_addrs()
    for interface_addresses in interfaces.values():
        for address in interface_addresses:
            if address.family == psutil.AF_LINK:
                return address.address
    return "Unknown"

def get_ip_address():
    """Fetches the primary IP address."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.error as e:
        log_error(f"IP retrieval error: {str(e)}")
        return "Unknown"

def get_domain_info():
    """Checks if the device is part of a domain and retrieves the domain name."""
    os_name = platform.system()
    commands = {
        "Windows": ['wmic', 'computersystem', 'get', 'domain'],
        "Linux": ['hostname', '-d'],
        "Darwin": ['hostname', '-d']
    }
    
    output = run_command(commands.get(os_name))
    if output:
        domain = output.split('\n')[1].strip()
        return domain if domain.lower() != "workgroup" else "No domain"
    return "Unknown"

# Hardware Information
def get_hardware_info():
    """Collects hardware information of the device."""
    return {
        'device_name': platform.node(),
        'device_company': get_device_manufacturer(),
        'device_model': get_device_model(),
        'device_naming_convention': get_device_naming_convention()
    }

def get_device_manufacturer():
    """Fetches the device manufacturer."""
    os_name = platform.system()
    commands = {
        "Windows": ['wmic', 'csproduct', 'get', 'vendor'],
        "Linux": ['cat', '/sys/devices/virtual/dmi/id/sys_vendor'],
        "Darwin": ['system_profiler', 'SPHardwareDataType']
    }
    
    output = run_command(commands.get(os_name))
    if output:
        return output.strip().split('\n')[1].strip()
    return "Unknown"

def get_device_model():
    """Fetches the device model."""
    os_name = platform.system()
    commands = {
        "Windows": ['wmic', 'csproduct', 'get', 'name'],
        "Linux": ['cat', '/sys/devices/virtual/dmi/id/product_name'],
        "Darwin": ['system_profiler', 'SPHardwareDataType']
    }
    
    output = run_command(commands.get(os_name))
    if output:
        return output.strip().split('\n')[1].strip()
    return "Unknown"

def get_device_naming_convention():
    """Provides a custom naming convention for the device."""
    return f"{platform.node()}-{platform.system()}{platform.release()}-{get_device_model()}"

# Installed Applications
def get_installed_apps():
    """Fetches a list of installed applications."""
    os_name = platform.system()
    commands = {
        "Windows": ['wmic', 'product', 'get', 'name'],
        "Linux": ['dpkg-query', '-W', '--showformat=${Package}\\n'],
        "Darwin": ['system_profiler', 'SPApplicationsDataType']
    }
    
    output = run_command(commands.get(os_name))
    if output:
        return parse_installed_apps(output, os_name)
    return ["Unable to retrieve installed apps"]

def parse_installed_apps(output, os_name):
    """Parses installed applications based on OS."""
    os_parsers = {
        "Windows": lambda x: [line.strip() for line in x.split("\n")[1:] if line.strip()],
        "Linux": lambda x: x.split("\n"),
        "Darwin": lambda x: [line.strip() for line in x.splitlines() if "Location" in line]
    }
    return os_parsers[os_name](output)

# API Service
def send_device_data(api_url, data, headers=None):
    """Sends collected device data to the specified API endpoint."""
    try:
        response = requests.post(api_url, json=data, headers=headers, verify=False)  # Disable SSL verification
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_error(f"API request failed: {str(e)}")
        return {"error": str(e)}

def get_device_info():
    """Collects all device information (system, network, hardware, and installed apps)."""
    device_info = {
        'system_info': get_system_info(),
        'network_info': get_network_info(),
        'hardware_info': get_hardware_info(),
        'installed_apps': get_installed_apps(),
    }
    return device_info

# Main Client Application
def run_client_app():
    """Main function to collect and send data to the web portal."""
    while True:
        try:
            device_data = get_device_info()
            response = send_device_data(API_URL, device_data, HEADERS)
            print(f"Server Response: {response}")
        except Exception as e:
            log_error(f"Unexpected error: {str(e)}")
        time.sleep(INTERVAL)

# Startup Configuration
def install_app():
    """Installs the application and sets it to run on startup."""
    if platform.system() == "Windows":
        add_to_startup_windows()
    elif platform.system() == "Linux":
        add_to_startup_linux()
    else:
        log_error("Unsupported OS for startup configuration.")

def add_to_startup_windows():
    """Adds the app to Windows startup using the registry."""
    try:
        script_path = os.path.abspath('InfoGetter.exe')
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "ClientApp", 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(key)
        print("Added to Windows startup successfully.")
    except Exception as e:
        log_error(f"Failed to add to Windows startup: {str(e)}")

def add_to_startup_linux():
    """Adds the app to Linux startup using cron jobs."""
    try:
        user = os.getenv('USER')
        script_path = os.path.abspath('InfoGetter.exe')
        cron_job = f"@reboot {script_path}"

        existing_crontab = os.popen(f'crontab -u {user} -l 2>/dev/null').read()
        if cron_job not in existing_crontab:
            os.system(f'(crontab -u {user} -l 2>/dev/null; echo "{cron_job}") | crontab -u {user} -')
            print("Added to Linux startup successfully.")
    except Exception as e:
        log_error(f"Failed to add to Linux startup: {str(e)}")

if __name__ == "__main__":
    install_app()
    run_client_app()
