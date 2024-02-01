import subprocess

def change_mac(interface, new_mac):
    print(f"Changing MAC address of {interface} to {new_mac}")

    # Disable the interface
    subprocess.call(["ifconfig", interface, "down"])

    # Change the MAC address
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])

    # Enable the interface
    subprocess.call(["ifconfig", interface, "up"])

# Example usage:
if __name__ == "__main__":
    interface = input("Enter the interface name (e.g., eth0, wlan0): ")
    new_mac = input("Enter the new MAC address: ")

    change_mac(interface, new_mac)

