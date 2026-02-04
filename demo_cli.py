#!/usr/bin/env python3
"""
Demo script to show the CLI interactive menu structure
This creates a mock demonstration of the menu system
"""
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def show_main_menu():
    clear_screen()
    print_header("Mobile Proxy Manager - Main Menu")
    print("  1. Devices Management")
    print("  2. Connections Management")
    print("  3. Quick Actions")
    print("  0. Exit")
    print()

def show_devices_menu():
    clear_screen()
    print_header("Devices Management")
    print("  1. List Connected Devices")
    print("  2. Refresh Device List")
    print("  3. Check Device IP")
    print("  4. Change Device IP")
    print("  5. View Device Details")
    print("  0. Back to Main Menu")
    print()

def show_connections_menu():
    clear_screen()
    print_header("Connections Management")
    print("  1. List All Connections")
    print("  2. Add New Connection")
    print("  3. Start Connection")
    print("  4. Stop Connection")
    print("  5. Delete Connection")
    print("  6. View Connection Details")
    print("  0. Back to Main Menu")
    print()

def show_quick_actions_menu():
    clear_screen()
    print_header("Quick Actions")
    print("  1. Start All Connections")
    print("  2. Stop All Connections")
    print("  3. Check All IPs")
    print("  4. Show System Status")
    print("  0. Back to Main Menu")
    print()

def show_list_devices():
    clear_screen()
    print_header("Connected Devices")
    print("Found 2 device(s):\n")
    print("1. Samsung Galaxy S21 (R5CR20ABCDE)")
    print("   Android Version: 13\n")
    print("2. Google Pixel 6 (1A234B5C6D7E)")
    print("   Android Version: 14\n")
    print("\nPress Enter to continue...")
    time.sleep(2)

def show_list_connections():
    clear_screen()
    print_header("All Connections")
    print("Found 2 connection(s):\n")
    print("Connection ID: 1")
    print("  Device: R5CR20ABCDE")
    print("  Ports: localhost:9090 -> device:8080")
    print("  Status: active")
    print("  Current IP: 192.168.1.100")
    print("  Last Check: 2024-01-15 10:30:45\n")
    print("Connection ID: 2")
    print("  Device: 1A234B5C6D7E")
    print("  Ports: localhost:9091 -> device:8080")
    print("  Status: stopped")
    print("  Current IP: 192.168.1.101")
    print("  Last Check: 2024-01-15 09:15:22\n")
    print("\nPress Enter to continue...")
    time.sleep(2)

def show_system_status():
    clear_screen()
    print_header("System Status")
    print("ADB Status: ✓ Available")
    print("Connected Devices: 2")
    print("Total Connections: 2")
    print("  Active: 1")
    print("  Stopped: 1")
    print("\nPress Enter to continue...")
    time.sleep(2)

def main():
    print("=" * 60)
    print("  Mobile Proxy Manager - CLI Interactive Mode Demo")
    print("=" * 60)
    print("\nThis demo shows the menu structure of the CLI mode.\n")
    print("Press Ctrl+C to exit at any time.\n")
    input("Press Enter to start the demo...")
    
    try:
        # Show main menu
        show_main_menu()
        time.sleep(2)
        
        # Navigate to Devices menu
        print("Navigating to Devices Management...")
        time.sleep(1)
        show_devices_menu()
        time.sleep(2)
        
        # Show list devices
        print("Selecting: List Connected Devices...")
        time.sleep(1)
        show_list_devices()
        
        # Back to devices menu
        show_devices_menu()
        time.sleep(1)
        
        # Back to main menu
        print("Returning to Main Menu...")
        time.sleep(1)
        show_main_menu()
        time.sleep(2)
        
        # Navigate to Connections menu
        print("Navigating to Connections Management...")
        time.sleep(1)
        show_connections_menu()
        time.sleep(2)
        
        # Show list connections
        print("Selecting: List All Connections...")
        time.sleep(1)
        show_list_connections()
        
        # Back to connections menu
        show_connections_menu()
        time.sleep(1)
        
        # Back to main menu
        print("Returning to Main Menu...")
        time.sleep(1)
        show_main_menu()
        time.sleep(2)
        
        # Navigate to Quick Actions
        print("Navigating to Quick Actions...")
        time.sleep(1)
        show_quick_actions_menu()
        time.sleep(2)
        
        # Show system status
        print("Selecting: Show System Status...")
        time.sleep(1)
        show_system_status()
        
        # Back to quick actions menu
        show_quick_actions_menu()
        time.sleep(1)
        
        # Back to main menu
        print("Returning to Main Menu...")
        time.sleep(1)
        show_main_menu()
        time.sleep(1)
        
        # Exit
        print("Exiting...")
        time.sleep(1)
        clear_screen()
        print("\n✅ Demo completed!\n")
        print("To run the actual interactive CLI mode:")
        print("  python cli.py interactive")
        print("  or")
        print("  python cli.py -i\n")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")

if __name__ == '__main__':
    main()
