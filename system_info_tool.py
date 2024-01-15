import platform
import psutil

def get_system_information():
    system_info = {
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
        'CPU Cores': psutil.cpu_count(logical=False),
        'Total CPU Threads': psutil.cpu_count(logical=True),
        'RAM Total': round(psutil.virtual_memory().total / (1024 ** 3), 2),  # in GB
        'RAM Used': round(psutil.virtual_memory().used / (1024 ** 3), 2),  # in GB
        'RAM Free': round(psutil.virtual_memory().free / (1024 ** 3), 2),  # in GB
        'Disk Total': round(psutil.disk_usage('/').total / (1024 ** 3), 2),  # in GB
        'Disk Used': round(psutil.disk_usage('/').used / (1024 ** 3), 2),  # in GB
        'Disk Free': round(psutil.disk_usage('/').free / (1024 ** 3), 2),  # in GB
    }

    try:
        # Get network information
        network_info = psutil.net_if_addrs()
        system_info['Network Interfaces'] = {interface: [addr.address for addr in addrs] for interface, addrs in network_info.items()}
    except Exception as e:
        system_info['Network Interfaces'] = f"Error getting network information: {str(e)}"

    try:
        # Get battery information (if applicable)
        battery_info = psutil.sensors_battery()
        if battery_info:
            system_info['Battery'] = {
                'Percentage': battery_info.percent,
                'Plugged In': battery_info.power_plugged,
                'Charging': battery_info.ischarging,
                'Time Remaining': battery_info.secsleft if battery_info.power_plugged else None,
            }
    except Exception as e:
        system_info['Battery'] = f"Error getting battery information: {str(e)}"

    return system_info

def display_system_information(system_info):
    print("System Information:")
    for key, value in system_info.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

def main():
    system_info = get_system_information()
    display_system_information(system_info)

if __name__ == "__main__":
    main()
