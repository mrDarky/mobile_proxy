#!/usr/bin/env python3
"""
CLI tool for Mobile Proxy Manager
For headless operation and automation
"""
import argparse
import sys
import time
from database import Database
from adb_manager import ADBManager
from proxy_manager import ProxyManager


class InteractiveCLI:
    """Interactive CLI mode with menus and submenus"""
    
    def __init__(self):
        self.db = Database()
        self.adb = ADBManager()
        self.proxy = ProxyManager(self.adb)
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60 + "\n")
    
    def print_menu(self, title, options):
        """Print a menu with options"""
        self.print_header(title)
        for key, value in options.items():
            print(f"  {key}. {value}")
        print()
    
    def get_input(self, prompt="Enter choice: "):
        """Get user input"""
        return input(prompt).strip()
    
    def pause(self):
        """Pause and wait for user to press Enter"""
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        """Display main menu"""
        while self.running:
            self.clear_screen()
            self.print_menu("Mobile Proxy Manager - Main Menu", {
                "1": "Devices Management",
                "2": "Connections Management",
                "3": "Quick Actions",
                "0": "Exit"
            })
            
            choice = self.get_input()
            
            if choice == "1":
                self.devices_menu()
            elif choice == "2":
                self.connections_menu()
            elif choice == "3":
                self.quick_actions_menu()
            elif choice == "0":
                print("\nGoodbye!")
                self.running = False
            else:
                print("Invalid choice. Please try again.")
                self.pause()
    
    def devices_menu(self):
        """Display devices management menu"""
        while True:
            self.clear_screen()
            self.print_menu("Devices Management", {
                "1": "List Connected Devices",
                "2": "Refresh Device List",
                "3": "Check Device IP",
                "4": "Change Device IP",
                "5": "View Device Details",
                "0": "Back to Main Menu"
            })
            
            choice = self.get_input()
            
            if choice == "1":
                self.list_devices_action()
            elif choice == "2":
                self.refresh_devices_action()
            elif choice == "3":
                self.check_device_ip_action()
            elif choice == "4":
                self.change_device_ip_action()
            elif choice == "5":
                self.view_device_details_action()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
                self.pause()
    
    def connections_menu(self):
        """Display connections management menu"""
        while True:
            self.clear_screen()
            self.print_menu("Connections Management", {
                "1": "List All Connections",
                "2": "Add New Connection",
                "3": "Start Connection",
                "4": "Stop Connection",
                "5": "Delete Connection",
                "6": "View Connection Details",
                "0": "Back to Main Menu"
            })
            
            choice = self.get_input()
            
            if choice == "1":
                self.list_connections_action()
            elif choice == "2":
                self.add_connection_action()
            elif choice == "3":
                self.start_connection_action()
            elif choice == "4":
                self.stop_connection_action()
            elif choice == "5":
                self.delete_connection_action()
            elif choice == "6":
                self.view_connection_details_action()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
                self.pause()
    
    def quick_actions_menu(self):
        """Display quick actions menu"""
        while True:
            self.clear_screen()
            self.print_menu("Quick Actions", {
                "1": "Start All Connections",
                "2": "Stop All Connections",
                "3": "Check All IPs",
                "4": "Show System Status",
                "0": "Back to Main Menu"
            })
            
            choice = self.get_input()
            
            if choice == "1":
                self.start_all_connections_action()
            elif choice == "2":
                self.stop_all_connections_action()
            elif choice == "3":
                self.check_all_ips_action()
            elif choice == "4":
                self.show_system_status_action()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
                self.pause()
    
    # Device actions
    def list_devices_action(self):
        """List connected devices"""
        self.clear_screen()
        self.print_header("Connected Devices")
        
        devices = self.adb.get_connected_devices()
        
        if not devices:
            print("No devices connected.")
        else:
            print(f"Found {len(devices)} device(s):\n")
            for i, device in enumerate(devices, 1):
                print(f"{i}. {device['model']} ({device['serial']})")
                print(f"   Android Version: {device['android_version']}")
                print()
        
        self.pause()
    
    def refresh_devices_action(self):
        """Refresh device list"""
        self.clear_screen()
        self.print_header("Refreshing Devices")
        
        print("Scanning for connected devices...")
        devices = self.adb.get_connected_devices()
        
        # Update database
        for device in devices:
            self.db.add_device(
                device['serial'],
                device['model'],
                device['android_version']
            )
        
        print(f"✓ Found and registered {len(devices)} device(s)")
        self.pause()
    
    def check_device_ip_action(self):
        """Check device IP"""
        self.clear_screen()
        self.print_header("Check Device IP")
        
        devices = self.adb.get_connected_devices()
        if not devices:
            print("No devices connected.")
            self.pause()
            return
        
        print("Available devices:")
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device['serial']} ({device['model']})")
        
        choice = self.get_input("\nEnter device number (0 to cancel): ")
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(devices):
                serial = devices[idx]['serial']
                print(f"\nChecking IP for {serial}...")
                ip = self.adb.get_device_ip(serial)
                
                if ip:
                    print(f"✓ Device IP: {ip}")
                else:
                    print("✗ Could not retrieve device IP")
            else:
                print("Invalid device number")
        except ValueError:
            print("Invalid input")
        
        self.pause()
    
    def change_device_ip_action(self):
        """Change device IP"""
        self.clear_screen()
        self.print_header("Change Device IP")
        
        devices = self.adb.get_connected_devices()
        if not devices:
            print("No devices connected.")
            self.pause()
            return
        
        print("Available devices:")
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device['serial']} ({device['model']})")
        
        choice = self.get_input("\nEnter device number (0 to cancel): ")
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(devices):
                serial = devices[idx]['serial']
                print(f"\nToggling airplane mode on {serial}...")
                
                success = self.adb.toggle_airplane_mode(serial, wait_time=5)
                
                if success:
                    print("✓ Airplane mode toggled successfully")
                    time.sleep(2)
                    print("\nChecking new IP...")
                    ip = self.adb.get_device_ip(serial)
                    if ip:
                        print(f"✓ New IP: {ip}")
                    else:
                        print("✗ Could not retrieve new IP")
                else:
                    print("✗ Failed to toggle airplane mode")
            else:
                print("Invalid device number")
        except ValueError:
            print("Invalid input")
        
        self.pause()
    
    def view_device_details_action(self):
        """View device details"""
        self.clear_screen()
        self.print_header("Device Details")
        
        devices = self.db.get_devices()
        if not devices:
            print("No devices in database.")
            self.pause()
            return
        
        print("Registered devices:")
        for i, device in enumerate(devices, 1):
            device_id, serial, model, android_version, status, last_seen = device
            print(f"{i}. {model} ({serial})")
        
        choice = self.get_input("\nEnter device number (0 to cancel): ")
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(devices):
                device_id, serial, model, android_version, status, last_seen = devices[idx]
                print(f"\nDevice Details:")
                print(f"  ID: {device_id}")
                print(f"  Serial: {serial}")
                print(f"  Model: {model}")
                print(f"  Android Version: {android_version}")
                print(f"  Status: {status}")
                print(f"  Last Seen: {last_seen}")
                
                # Get current IP
                ip = self.adb.get_device_ip(serial)
                if ip:
                    print(f"  Current IP: {ip}")
            else:
                print("Invalid device number")
        except ValueError:
            print("Invalid input")
        
        self.pause()
    
    # Connection actions
    def list_connections_action(self):
        """List all connections"""
        self.clear_screen()
        self.print_header("All Connections")
        
        connections = self.db.get_connections()
        
        if not connections:
            print("No connections configured.")
        else:
            print(f"Found {len(connections)} connection(s):\n")
            for conn in connections:
                conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
                print(f"Connection ID: {conn_id}")
                print(f"  Device: {serial}")
                print(f"  Ports: localhost:{local_port} -> device:{remote_port}")
                print(f"  Status: {status}")
                print(f"  Current IP: {current_ip or 'Unknown'}")
                print(f"  Last Check: {last_check or 'Never'}")
                print()
        
        self.pause()
    
    def add_connection_action(self):
        """Add new connection"""
        self.clear_screen()
        self.print_header("Add New Connection")
        
        devices = self.adb.get_connected_devices()
        if not devices:
            print("No devices connected. Please connect a device first.")
            self.pause()
            return
        
        print("Available devices:")
        for i, device in enumerate(devices, 1):
            print(f"{i}. {device['serial']} ({device['model']})")
        
        choice = self.get_input("\nEnter device number (0 to cancel): ")
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(devices):
                device = devices[idx]
                serial = device['serial']
                
                local_port = self.get_input("Enter local port (e.g., 9090): ")
                remote_port = self.get_input("Enter remote port (e.g., 8080): ")
                
                try:
                    local_port = int(local_port)
                    remote_port = int(remote_port)
                    
                    if local_port <= 0 or local_port > 65535 or remote_port <= 0 or remote_port > 65535:
                        print("✗ Port numbers must be between 1 and 65535")
                    else:
                        # Add device to database
                        device_id = self.db.add_device(device['serial'], device['model'], device['android_version'])
                        
                        # Add connection
                        conn_id = self.db.add_connection(device_id, local_port, remote_port)
                        
                        if conn_id:
                            print(f"✓ Connection added successfully (ID: {conn_id})")
                        else:
                            print("✗ Failed to add connection (port may be in use)")
                except ValueError:
                    print("✗ Invalid port numbers")
            else:
                print("Invalid device number")
        except ValueError:
            print("Invalid input")
        
        self.pause()
    
    def start_connection_action(self):
        """Start a connection"""
        self.clear_screen()
        self.print_header("Start Connection")
        
        connections = self.db.get_connections()
        if not connections:
            print("No connections configured.")
            self.pause()
            return
        
        print("Available connections:")
        for conn in connections:
            conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
            print(f"{conn_id}. {serial} - localhost:{local_port} -> device:{remote_port} [{status}]")
        
        choice = self.get_input("\nEnter connection ID (0 to cancel): ")
        
        if choice == "0":
            return
        
        try:
            conn_id = int(choice)
            conn = next((c for c in connections if c[0] == conn_id), None)
            
            if conn:
                _, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
                
                if status == 'active':
                    print(f"Connection {conn_id} is already active")
                else:
                    print(f"Starting connection {conn_id}...")
                    success = self.proxy.start_proxy(serial, local_port, remote_port)
                    
                    if success:
                        self.db.update_connection_status(conn_id, 'active')
                        print(f"✓ Connection {conn_id} started successfully")
                    else:
                        print(f"✗ Failed to start connection {conn_id}")
            else:
                print("Connection not found")
        except ValueError:
            print("Invalid input")
        
        self.pause()
    
    def stop_connection_action(self):
        """Stop a connection"""
        self.clear_screen()
        self.print_header("Stop Connection")
        
        connections = self.db.get_connections()
        if not connections:
            print("No connections configured.")
            self.pause()
            return
        
        print("Available connections:")
        for conn in connections:
            conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
            print(f"{conn_id}. {serial} - localhost:{local_port} -> device:{remote_port} [{status}]")
        
        choice = self.get_input("\nEnter connection ID (0 to cancel): ")
        
        if choice == "0":
            return
        
        try:
            conn_id = int(choice)
            conn = next((c for c in connections if c[0] == conn_id), None)
            
            if conn:
                _, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
                
                if status == 'stopped':
                    print(f"Connection {conn_id} is already stopped")
                else:
                    print(f"Stopping connection {conn_id}...")
                    success = self.proxy.stop_proxy(serial, local_port)
                    
                    if success:
                        self.db.update_connection_status(conn_id, 'stopped')
                        print(f"✓ Connection {conn_id} stopped successfully")
                    else:
                        print(f"✗ Failed to stop connection {conn_id}")
            else:
                print("Connection not found")
        except ValueError:
            print("Invalid input")
        
        self.pause()
    
    def delete_connection_action(self):
        """Delete a connection"""
        self.clear_screen()
        self.print_header("Delete Connection")
        
        connections = self.db.get_connections()
        if not connections:
            print("No connections configured.")
            self.pause()
            return
        
        print("Available connections:")
        for conn in connections:
            conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
            print(f"{conn_id}. {serial} - localhost:{local_port} -> device:{remote_port} [{status}]")
        
        choice = self.get_input("\nEnter connection ID (0 to cancel): ")
        
        if choice == "0":
            return
        
        try:
            conn_id = int(choice)
            conn = next((c for c in connections if c[0] == conn_id), None)
            
            if conn:
                confirm = self.get_input(f"Are you sure you want to delete connection {conn_id}? (yes/no): ")
                
                if confirm.lower() in ['yes', 'y']:
                    # Stop connection if active
                    _, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
                    if status == 'active':
                        self.proxy.stop_proxy(serial, local_port)
                    
                    # Delete from database
                    self.db.delete_connection(conn_id)
                    print(f"✓ Connection {conn_id} deleted successfully")
                else:
                    print("Deletion cancelled")
            else:
                print("Connection not found")
        except ValueError:
            print("Invalid input")
        
        self.pause()
    
    def view_connection_details_action(self):
        """View connection details"""
        self.clear_screen()
        self.print_header("Connection Details")
        
        connections = self.db.get_connections()
        if not connections:
            print("No connections configured.")
            self.pause()
            return
        
        print("Available connections:")
        for conn in connections:
            conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
            print(f"{conn_id}. {serial} - localhost:{local_port} -> device:{remote_port}")
        
        choice = self.get_input("\nEnter connection ID (0 to cancel): ")
        
        if choice == "0":
            return
        
        try:
            conn_id = int(choice)
            conn = next((c for c in connections if c[0] == conn_id), None)
            
            if conn:
                conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
                print(f"\nConnection Details:")
                print(f"  Connection ID: {conn_id}")
                print(f"  Device ID: {device_id}")
                print(f"  Device Serial: {serial}")
                print(f"  Local Port: {local_port}")
                print(f"  Remote Port: {remote_port}")
                print(f"  Status: {status}")
                print(f"  Current IP: {current_ip or 'Unknown'}")
                print(f"  Last Check: {last_check or 'Never'}")
            else:
                print("Connection not found")
        except ValueError:
            print("Invalid input")
        
        self.pause()
    
    # Quick actions
    def start_all_connections_action(self):
        """Start all connections"""
        self.clear_screen()
        self.print_header("Start All Connections")
        
        connections = self.db.get_connections()
        if not connections:
            print("No connections configured.")
            self.pause()
            return
        
        started = 0
        failed = 0
        
        for conn in connections:
            conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
            
            if status == 'stopped':
                print(f"Starting connection {conn_id} ({serial})...")
                success = self.proxy.start_proxy(serial, local_port, remote_port)
                
                if success:
                    self.db.update_connection_status(conn_id, 'active')
                    started += 1
                    print(f"  ✓ Started")
                else:
                    failed += 1
                    print(f"  ✗ Failed")
        
        print(f"\nSummary: {started} started, {failed} failed")
        self.pause()
    
    def stop_all_connections_action(self):
        """Stop all connections"""
        self.clear_screen()
        self.print_header("Stop All Connections")
        
        connections = self.db.get_connections()
        if not connections:
            print("No connections configured.")
            self.pause()
            return
        
        stopped = 0
        failed = 0
        
        for conn in connections:
            conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
            
            if status == 'active':
                print(f"Stopping connection {conn_id} ({serial})...")
                success = self.proxy.stop_proxy(serial, local_port)
                
                if success:
                    self.db.update_connection_status(conn_id, 'stopped')
                    stopped += 1
                    print(f"  ✓ Stopped")
                else:
                    failed += 1
                    print(f"  ✗ Failed")
        
        print(f"\nSummary: {stopped} stopped, {failed} failed")
        self.pause()
    
    def check_all_ips_action(self):
        """Check IPs for all devices"""
        self.clear_screen()
        self.print_header("Check All Device IPs")
        
        devices = self.adb.get_connected_devices()
        if not devices:
            print("No devices connected.")
            self.pause()
            return
        
        for device in devices:
            serial = device['serial']
            model = device['model']
            print(f"Checking {model} ({serial})...")
            
            ip = self.adb.get_device_ip(serial)
            if ip:
                print(f"  ✓ IP: {ip}")
            else:
                print(f"  ✗ Could not retrieve IP")
        
        self.pause()
    
    def show_system_status_action(self):
        """Show system status"""
        self.clear_screen()
        self.print_header("System Status")
        
        # Check ADB
        adb_available = self.adb.check_adb_available()
        print(f"ADB Status: {'✓ Available' if adb_available else '✗ Not Available'}")
        
        # Count devices
        devices = self.adb.get_connected_devices()
        print(f"Connected Devices: {len(devices)}")
        
        # Count connections
        connections = self.db.get_connections()
        active_connections = sum(1 for c in connections if c[5] == 'active')
        stopped_connections = sum(1 for c in connections if c[5] == 'stopped')
        
        print(f"Total Connections: {len(connections)}")
        print(f"  Active: {active_connections}")
        print(f"  Stopped: {stopped_connections}")
        
        self.pause()
    
    def run(self):
        """Run the interactive CLI"""
        # Check ADB availability
        if not self.adb.check_adb_available():
            print("Error: ADB is not installed or not in PATH")
            print("Please install Android Debug Bridge (ADB) to use this application.")
            return 1
        
        self.main_menu()
        return 0


def list_devices(adb):
    """List connected devices"""
    devices = adb.get_connected_devices()
    
    if not devices:
        print("No devices connected.")
        return
    
    print(f"\nConnected Devices ({len(devices)}):")
    print("-" * 60)
    for i, device in enumerate(devices, 1):
        print(f"{i}. {device['model']} ({device['serial']})")
        print(f"   Android: {device['android_version']}")
    print()


def list_connections(db):
    """List all connections"""
    connections = db.get_connections()
    
    if not connections:
        print("No connections configured.")
        return
    
    print(f"\nConfigured Connections ({len(connections)}):")
    print("-" * 80)
    for conn in connections:
        conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
        print(f"ID: {conn_id} | {serial}")
        print(f"  localhost:{local_port} -> device:{remote_port}")
        print(f"  Status: {status} | IP: {current_ip or 'Unknown'}")
    print()


def add_connection(db, adb, serial, local_port, remote_port):
    """Add a new connection"""
    # Get device info
    devices = adb.get_connected_devices()
    device = next((d for d in devices if d['serial'] == serial), None)
    
    if not device:
        print(f"Error: Device {serial} not found")
        return False
    
    # Add device to database
    device_id = db.add_device(device['serial'], device['model'], device['android_version'])
    
    # Add connection
    conn_id = db.add_connection(device_id, local_port, remote_port)
    
    if conn_id:
        print(f"✓ Connection added (ID: {conn_id})")
        return True
    else:
        print(f"✗ Failed to add connection (port may be in use)")
        return False


def start_connection(db, proxy, conn_id):
    """Start a connection"""
    connections = db.get_connections()
    conn = next((c for c in connections if c[0] == conn_id), None)
    
    if not conn:
        print(f"Error: Connection {conn_id} not found")
        return False
    
    conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
    
    success = proxy.start_proxy(serial, local_port, remote_port)
    
    if success:
        db.update_connection_status(conn_id, 'active')
        print(f"✓ Connection {conn_id} started")
        return True
    else:
        print(f"✗ Failed to start connection {conn_id}")
        return False


def stop_connection(db, proxy, conn_id):
    """Stop a connection"""
    connections = db.get_connections()
    conn = next((c for c in connections if c[0] == conn_id), None)
    
    if not conn:
        print(f"Error: Connection {conn_id} not found")
        return False
    
    conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
    
    success = proxy.stop_proxy(serial, local_port)
    
    if success:
        db.update_connection_status(conn_id, 'stopped')
        print(f"✓ Connection {conn_id} stopped")
        return True
    else:
        print(f"✗ Failed to stop connection {conn_id}")
        return False


def check_ip(adb, serial):
    """Check device IP"""
    ip = adb.get_device_ip(serial)
    
    if ip:
        print(f"Device IP: {ip}")
        return ip
    else:
        print("Could not retrieve device IP")
        return None


def change_ip(adb, serial, wait_time=5):
    """Change device IP by toggling airplane mode"""
    print(f"Toggling airplane mode on {serial}...")
    
    success = adb.toggle_airplane_mode(serial, wait_time)
    
    if success:
        print("✓ Airplane mode toggled successfully")
        time.sleep(2)
        new_ip = check_ip(adb, serial)
        return True
    else:
        print("✗ Failed to toggle airplane mode")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Mobile Proxy Manager CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    %(prog)s interactive
    %(prog)s -i
  
  List devices:
    %(prog)s list-devices
  
  List connections:
    %(prog)s list-connections
  
  Add connection:
    %(prog)s add ABC123 9090 8080
  
  Start connection:
    %(prog)s start 1
  
  Stop connection:
    %(prog)s stop 1
  
  Check device IP:
    %(prog)s check-ip ABC123
  
  Change device IP:
    %(prog)s change-ip ABC123
        """
    )
    
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode with menus')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Interactive mode
    subparsers.add_parser('interactive', help='Run in interactive mode with menus')
    
    # List devices
    subparsers.add_parser('list-devices', help='List connected devices')
    
    # List connections
    subparsers.add_parser('list-connections', help='List configured connections')
    
    # Add connection
    add_parser = subparsers.add_parser('add', help='Add a new connection')
    add_parser.add_argument('serial', help='Device serial number')
    add_parser.add_argument('local_port', type=int, help='Local port')
    add_parser.add_argument('remote_port', type=int, help='Remote port')
    
    # Start connection
    start_parser = subparsers.add_parser('start', help='Start a connection')
    start_parser.add_argument('connection_id', type=int, help='Connection ID')
    
    # Stop connection
    stop_parser = subparsers.add_parser('stop', help='Stop a connection')
    stop_parser.add_argument('connection_id', type=int, help='Connection ID')
    
    # Check IP
    check_parser = subparsers.add_parser('check-ip', help='Check device IP')
    check_parser.add_argument('serial', help='Device serial number')
    
    # Change IP
    change_parser = subparsers.add_parser('change-ip', help='Change device IP')
    change_parser.add_argument('serial', help='Device serial number')
    change_parser.add_argument('--wait', type=int, default=5, help='Wait time between toggles')
    
    args = parser.parse_args()
    
    # Check if interactive mode is requested
    if args.interactive or args.command == 'interactive':
        cli = InteractiveCLI()
        return cli.run()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize components
    db = Database()
    adb = ADBManager()
    proxy = ProxyManager(adb)
    
    # Check ADB availability
    if not adb.check_adb_available():
        print("Error: ADB is not installed or not in PATH")
        return 1
    
    # Execute command
    try:
        if args.command == 'list-devices':
            list_devices(adb)
        
        elif args.command == 'list-connections':
            list_connections(db)
        
        elif args.command == 'add':
            success = add_connection(db, adb, args.serial, args.local_port, args.remote_port)
            return 0 if success else 1
        
        elif args.command == 'start':
            success = start_connection(db, proxy, args.connection_id)
            return 0 if success else 1
        
        elif args.command == 'stop':
            success = stop_connection(db, proxy, args.connection_id)
            return 0 if success else 1
        
        elif args.command == 'check-ip':
            ip = check_ip(adb, args.serial)
            return 0 if ip else 1
        
        elif args.command == 'change-ip':
            success = change_ip(adb, args.serial, args.wait)
            return 0 if success else 1
        
        else:
            parser.print_help()
            return 1
    
    except KeyboardInterrupt:
        print("\nOperation cancelled")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
