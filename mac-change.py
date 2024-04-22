# written by zlite4 if you like this app please donate to my cash app $zlite4

import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import random
import string


class MacChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MAC Address Changer")

        self.interface_label = tk.Label(root, text="Enter Interface Name:")
        self.interface_label.pack()

        self.interface_entry = tk.Entry(root)
        self.interface_entry.pack()

        self.current_mac_label = tk.Label(root, text="Current MAC Address:")
        self.current_mac_label.pack()

        self.current_mac_value = tk.Label(root, text="")
        self.current_mac_value.pack()

        self.new_mac_label = tk.Label(root, text="Enter New MAC Address:")
        self.new_mac_label.pack()

        self.new_mac_entry = tk.Entry(root)
        self.new_mac_entry.pack()

        self.change_mac_button = tk.Button(root, text="Change MAC Address", command=self.change_mac)
        self.change_mac_button.pack()

        self.revert_button = tk.Button(root, text="Revert to Original MAC", command=self.revert_mac)
        self.revert_button.pack()

        self.random_mac_button = tk.Button(root, text="Generate Random MAC", command=self.generate_random_mac)
        self.random_mac_button.pack()

    def get_current_mac(self):
        interface = self.interface_entry.get()
        try:
            result = subprocess.check_output(["ifconfig", interface])
            mac_address = self.extract_mac(result.decode())
            return mac_address
        except subprocess.CalledProcessError:
            return None

    def extract_mac(self, ifconfig_output):
        mac_index = ifconfig_output.find("ether") + 6
        return ifconfig_output[mac_index:mac_index + 17]

    def change_mac(self):
        interface = self.interface_entry.get()
        new_mac = self.new_mac_entry.get()
        if new_mac:
            subprocess.run(["sudo", "ifconfig", interface, "down"])
            subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
            subprocess.run(["sudo", "ifconfig", interface, "up"])
            messagebox.showinfo("Success", "MAC Address Changed Successfully!")
            self.update_current_mac()
        else:
            messagebox.showerror("Error", "Please Enter a Valid MAC Address")

    def revert_mac(self):
        interface = self.interface_entry.get()
        original_mac = self.get_current_mac()
        if original_mac:
            subprocess.run(["sudo", "ifconfig", interface, "down"])
            subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", original_mac])
            subprocess.run(["sudo", "ifconfig", interface, "up"])
            messagebox.showinfo("Success", "MAC Address Reverted Successfully!")
            self.update_current_mac()
        else:
            messagebox.showerror("Error", "Could Not Retrieve Original MAC Address")

    def generate_random_mac(self):
        random_mac = ':'.join([''.join(random.choices(string.hexdigits.upper(), k=2)) for _ in range(6)])
        self.new_mac_entry.delete(0, tk.END)
        self.new_mac_entry.insert(tk.END, random_mac)

    def update_current_mac(self):
        current_mac = self.get_current_mac()
        if current_mac:
            self.current_mac_value.config(text=current_mac)
        else:
            self.current_mac_value.config(text="Not Found")


if __name__ == "__main__":
    root = tk.Tk()
    app = MacChangerApp(root)
    root.mainloop()
