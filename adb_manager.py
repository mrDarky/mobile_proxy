"""
ADB Manager module for detecting and managing Android devices
"""
import subprocess
import re
import time


class ADBManager:
    def __init__(self):
        self.devices = {}
    
    def check_adb_available(self):
        """Check if ADB is available in the system"""
        try:
            result = subprocess.run(['adb', 'version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_connected_devices(self):
        """Get list of connected Android devices"""
        try:
            result = subprocess.run(['adb', 'devices', '-l'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            
            if result.returncode != 0:
                return []
            
            devices = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip first line "List of devices attached"
            
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2 and parts[1] == 'device':
                        serial = parts[0]
                        
                        # Get device model and Android version
                        model = self.get_device_property(serial, 'ro.product.model')
                        android_version = self.get_device_property(serial, 'ro.build.version.release')
                        
                        devices.append({
                            'serial': serial,
                            'model': model,
                            'android_version': android_version
                        })
            
            return devices
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def get_device_property(self, serial, prop_name):
        """Get a property from a device"""
        try:
            result = subprocess.run(['adb', '-s', serial, 'shell', 'getprop', prop_name],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
            return ''
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return ''
    
    def create_port_forward(self, serial, local_port, remote_port):
        """Create ADB port forwarding"""
        try:
            # First, remove any existing forwarding on this local port
            subprocess.run(['adb', '-s', serial, 'forward', '--remove', f'tcp:{local_port}'],
                         capture_output=True,
                         timeout=5)
            
            # Create new port forwarding
            result = subprocess.run(['adb', '-s', serial, 'forward', 
                                   f'tcp:{local_port}', f'tcp:{remote_port}'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def remove_port_forward(self, serial, local_port):
        """Remove ADB port forwarding"""
        try:
            result = subprocess.run(['adb', '-s', serial, 'forward', '--remove', f'tcp:{local_port}'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def list_port_forwards(self, serial):
        """List all port forwards for a device"""
        try:
            result = subprocess.run(['adb', '-s', serial, 'forward', '--list'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            
            if result.returncode == 0:
                forwards = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip() and serial in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            forwards.append({
                                'local': parts[1],
                                'remote': parts[2]
                            })
                return forwards
            return []
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def enable_airplane_mode(self, serial):
        """Enable airplane mode on device"""
        try:
            # Enable airplane mode
            subprocess.run(['adb', '-s', serial, 'shell', 'settings', 'put', 'global', 
                          'airplane_mode_on', '1'],
                         capture_output=True,
                         timeout=5)
            
            # Broadcast the change
            subprocess.run(['adb', '-s', serial, 'shell', 'am', 'broadcast', 
                          '-a', 'android.intent.action.AIRPLANE_MODE', 
                          '--ez', 'state', 'true'],
                         capture_output=True,
                         timeout=5)
            
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def disable_airplane_mode(self, serial):
        """Disable airplane mode on device"""
        try:
            # Disable airplane mode
            subprocess.run(['adb', '-s', serial, 'shell', 'settings', 'put', 'global', 
                          'airplane_mode_on', '0'],
                         capture_output=True,
                         timeout=5)
            
            # Broadcast the change
            subprocess.run(['adb', '-s', serial, 'shell', 'am', 'broadcast', 
                          '-a', 'android.intent.action.AIRPLANE_MODE', 
                          '--ez', 'state', 'false'],
                         capture_output=True,
                         timeout=5)
            
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def toggle_airplane_mode(self, serial, wait_time=5):
        """Toggle airplane mode to change IP"""
        if self.enable_airplane_mode(serial):
            time.sleep(wait_time)
            if self.disable_airplane_mode(serial):
                time.sleep(wait_time)  # Wait for connection to restore
                return True
        return False
    
    def get_device_ip(self, serial):
        """Get device's IP address"""
        try:
            # Try to get IP from wlan0
            result = subprocess.run(['adb', '-s', serial, 'shell', 'ip', 'addr', 'show', 'wlan0'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            
            if result.returncode == 0:
                # Parse IP address from output
                match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
                if match:
                    return match.group(1)
            
            # Fallback: try getprop
            result = subprocess.run(['adb', '-s', serial, 'shell', 'getprop', 'dhcp.wlan0.ipaddress'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            
            return None
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None
