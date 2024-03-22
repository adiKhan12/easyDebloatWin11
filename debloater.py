import os
import subprocess
from colorama import Fore, Style
from colorama import init as colorama_init

# Initialize Colorama
colorama_init()

def run_powershell_command(command):
    """Runs a PowerShell command and returns the output."""
    return subprocess.run(["powershell", "-Command", command], capture_output=True, text=True).stdout

def list_apps():
    """Lists all bloatware apps."""
    return [
        "Microsoft.3DBuilder",
        "Microsoft.BingWeather",
        "Microsoft.Getstarted",
        "Microsoft.Messaging",
        "Microsoft.MicrosoftSolitaireCollection",
        "Microsoft.Office.OneNote",
        "Microsoft.OneConnect",
        "Microsoft.People",
        "Microsoft.SkypeApp",
        "Microsoft.Windows.Photos",
        "Microsoft.WindowsAlarms",
        "Microsoft.WindowsCalculator",
        "Microsoft.WindowsCamera",
        "microsoft.windowscommunicationsapps",  # Mail and Calendar
        "Microsoft.WindowsMaps",
        "Microsoft.WindowsSoundRecorder",
        "Microsoft.Xbox.TCUI",
        "Microsoft.XboxApp",
        "Microsoft.XboxGameOverlay",
        "Microsoft.XboxGamingOverlay",
        "Microsoft.XboxIdentityProvider",
        "Microsoft.XboxSpeechToTextOverlay",
        "Microsoft.YourPhone",
        "Microsoft.ZuneMusic",
        "Microsoft.ZuneVideo",
        # Further to be added
    ]


def list_services():
    """Lists services considered non-essential."""
    return [
        "XblGameSave",  # Xbox Live Game Save Service
        "XboxGipSvc",  # Xbox Accessory Management Service
        "XboxNetApiSvc",  # Xbox Live Networking Service
        "wsearch",  # Windows Search
        "PrintWorkflowUserSvc",  # Print Workflow Service
        "MapsBroker",  # Downloaded Maps Manager
        "lfsvc",  # Geolocation Service
        "CDPSvc",  # Connected Devices Platform Service
        "RetailDemo",  # Retail Demo Service
        "diagnosticshub.standardcollector.service",  # Microsoft Diagnostics Hub Standard Collector Service
        "DmwAppPushSvc",  # Device Management Wireless Application Protocol (WAP) Push message Routing Service
        # Further to be added
    ]


def check_installed_apps(apps):
    """Checks which apps are installed."""
    installed_apps = []
    for app in apps:
        if run_powershell_command(f"Get-AppxPackage -Name {app}"):
            installed_apps.append(app)
    return installed_apps

def check_running_services(services):
    """Checks which services are running."""
    running_services = []
    for service in services:
        if "Running" in run_powershell_command(f"Get-Service {service} | Select-Object -ExpandProperty Status"):
            running_services.append(service)
    return running_services

def user_selection(options, options_type):
    """Prompts the user to select options for removal."""
    print(f"\nSelect {options_type} to debloat (separated by commas, e.g., 1,2,3):")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")
    selections = input("> ").split(',')
    selected_options = [options[int(selection.strip()) - 1] for selection in selections if selection.strip().isdigit()]
    return selected_options

def remove_apps(apps):
    """Removes selected apps."""
    for app in apps:
        print(f"Removing {app}...")
        run_powershell_command(f"Get-AppxPackage *{app}* | Remove-AppxPackage")

def disable_services(services):
    """Disables and stops selected services."""
    for service in services:
        print(f"Disabling {service}...")
        run_powershell_command(f"Stop-Service -Name {service} -Force")
        run_powershell_command(f"Set-Service -Name {service} -StartupType Disabled")

def main():
    print(Fore.GREEN + "Windows 11 Debloater" + Style.RESET_ALL)

    # Apps
    apps = list_apps()
    installed_apps = check_installed_apps(apps)
    if installed_apps:
        print(Fore.YELLOW + "\nInstalled Apps:" + Style.RESET_ALL)
        selected_apps = user_selection(installed_apps, "apps")
        remove_apps(selected_apps)
    else:
        print(Fore.YELLOW + "\nNo known bloatware apps are installed." + Style.RESET_ALL)

    # Services
    services = list_services()
    running_services = check_running_services(services)
    if running_services:
        print(Fore.YELLOW + "\nRunning Services:" + Style.RESET_ALL)
        selected_services = user_selection(running_services, "services")
        disable_services(selected_services)
    else:
        print(Fore.YELLOW + "\nNo non-essential services are running." + Style.RESET_ALL)

    print(Fore.GREEN + "\nDebloating completed. Please restart your computer." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
