"""
Proxy Manager module for handling proxy connections and IP checking
"""
import socket
import threading
import requests
import time


class ProxyManager:
    def __init__(self, adb_manager):
        self.adb_manager = adb_manager
        self.active_forwards = {}
    
    def start_proxy(self, serial, local_port, remote_port):
        """Start a proxy connection"""
        success = self.adb_manager.create_port_forward(serial, local_port, remote_port)
        
        if success:
            self.active_forwards[local_port] = {
                'serial': serial,
                'remote_port': remote_port,
                'status': 'active'
            }
        
        return success
    
    def stop_proxy(self, serial, local_port):
        """Stop a proxy connection"""
        success = self.adb_manager.remove_port_forward(serial, local_port)
        
        if success and local_port in self.active_forwards:
            del self.active_forwards[local_port]
        
        return success
    
    def check_ip(self, timeout=10):
        """Check public IP address"""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=timeout)
            if response.status_code == 200:
                return response.json().get('ip')
        except Exception as e:
            print(f"Error checking IP: {e}")
        
        # Fallback to alternative service
        try:
            response = requests.get('https://ifconfig.me/ip', timeout=timeout)
            if response.status_code == 200:
                return response.text.strip()
        except Exception as e:
            print(f"Error checking IP (fallback): {e}")
        
        return None
    
    def check_connection(self, local_port, timeout=5):
        """Check if a connection on local_port is working"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex(('127.0.0.1', local_port))
            sock.close()
            return result == 0
        except Exception as e:
            print(f"Error checking connection on port {local_port}: {e}")
            return False
    
    def get_active_forwards(self):
        """Get all active port forwards"""
        return self.active_forwards.copy()
