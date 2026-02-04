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
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
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
