"""
Main application for Mobile Proxy Manager
Cross-platform app for creating proxy connections from mobile devices
"""
import sys
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty

from database import Database
from adb_manager import ADBManager
from proxy_manager import ProxyManager


class DeviceItem(BoxLayout):
    """Widget for displaying device information"""
    device_name = StringProperty('')
    serial = StringProperty('')
    android_version = StringProperty('')
    device_id = NumericProperty(0)
    
    def __init__(self, device_id, serial, model, android_version, callback, **kwargs):
        super().__init__(**kwargs)
        self.device_id = device_id
        self.serial = serial
        self.device_name = model or serial
        self.android_version = android_version
        self.callback = callback
    
    def on_add_connection(self):
        """Handle add connection button"""
        self.callback(self.device_id, self.serial)


class ConnectionItem(BoxLayout):
    """Widget for displaying connection information"""
    connection_id = NumericProperty(0)
    serial = StringProperty('')
    local_port = NumericProperty(0)
    remote_port = NumericProperty(0)
    status = StringProperty('stopped')
    current_ip = StringProperty('')
    
    def __init__(self, connection_id, device_id, serial, local_port, remote_port, 
                 status, current_ip, callbacks, **kwargs):
        super().__init__(**kwargs)
        self.connection_id = connection_id
        self.device_id = device_id
        self.serial = serial
        self.local_port = local_port
        self.remote_port = remote_port
        self.status = status
        self.current_ip = current_ip or ''
        self.callbacks = callbacks
    
    def on_toggle(self):
        """Handle toggle button"""
        self.callbacks['toggle'](self)
    
    def on_check_ip(self):
        """Handle check IP button"""
        self.callbacks['check_ip'](self)
    
    def on_change_ip(self):
        """Handle change IP button"""
        self.callbacks['change_ip'](self)


class MainLayout(BoxLayout):
    """Main application layout"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.adb = ADBManager()
        self.proxy = ProxyManager(self.adb)
        
        # Check if ADB is available
        if not self.adb.check_adb_available():
            Clock.schedule_once(lambda dt: self.show_error(
                "ADB Not Found",
                "ADB is not installed or not in PATH.\n"
                "Please install Android Debug Bridge (ADB) to use this application."
            ), 0.5)
        
        # Schedule periodic refresh
        Clock.schedule_interval(lambda dt: self.refresh_connections(), 10)
    
    def refresh_devices(self):
        """Refresh the list of connected devices"""
        devices = self.adb.get_connected_devices()
        
        # Update database
        for device in devices:
            self.db.add_device(
                device['serial'],
                device['model'],
                device['android_version']
            )
        
        # Update UI
        self.update_device_list()
    
    def update_device_list(self):
        """Update the device list UI"""
        device_list = self.ids.device_list
        device_list.clear_widgets()
        
        devices = self.db.get_devices()
        
        if not devices:
            label = Label(
                text='No devices connected.\nConnect a device via USB and enable USB debugging.',
                size_hint_y=None,
                height=100
            )
            device_list.add_widget(label)
        else:
            for device in devices:
                device_id, serial, model, android_version, status, last_seen = device
                
                item = DeviceItem(
                    device_id=device_id,
                    serial=serial,
                    model=model,
                    android_version=android_version,
                    callback=self.show_add_connection_dialog
                )
                device_list.add_widget(item)
    
    def refresh_connections(self):
        """Refresh the list of connections"""
        self.update_connection_list()
    
    def update_connection_list(self):
        """Update the connection list UI"""
        connection_list = self.ids.connection_list
        connection_list.clear_widgets()
        
        connections = self.db.get_connections()
        
        if not connections:
            label = Label(
                text='No connections configured.\nAdd a connection from a device.',
                size_hint_y=None,
                height=100
            )
            connection_list.add_widget(label)
        else:
            for conn in connections:
                conn_id, device_id, serial, local_port, remote_port, status, current_ip, last_check = conn
                
                callbacks = {
                    'toggle': self.toggle_connection,
                    'check_ip': self.check_connection_ip,
                    'change_ip': self.change_connection_ip
                }
                
                item = ConnectionItem(
                    connection_id=conn_id,
                    device_id=device_id,
                    serial=serial,
                    local_port=local_port,
                    remote_port=remote_port,
                    status=status,
                    current_ip=current_ip,
                    callbacks=callbacks
                )
                connection_list.add_widget(item)
    
    def show_add_connection_dialog(self, device_id, serial):
        """Show dialog to add a new connection"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(text=f'Add connection for device: {serial}'))
        
        local_port_input = TextInput(
            hint_text='Local port (e.g., 8080)',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        content.add_widget(local_port_input)
        
        remote_port_input = TextInput(
            hint_text='Remote port (e.g., 8080)',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        content.add_widget(remote_port_input)
        
        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        popup = Popup(
            title='Add Connection',
            content=content,
            size_hint=(0.8, 0.4)
        )
        
        def add_connection(instance):
            try:
                local_port = int(local_port_input.text)
                remote_port = int(remote_port_input.text)
                
                if local_port <= 0 or local_port > 65535 or remote_port <= 0 or remote_port > 65535:
                    self.show_error('Invalid Port', 'Port numbers must be between 1 and 65535')
                    return
                
                conn_id = self.db.add_connection(device_id, local_port, remote_port)
                
                if conn_id:
                    popup.dismiss()
                    self.refresh_connections()
                else:
                    self.show_error('Error', 'Failed to add connection. Port may already be in use.')
            except ValueError:
                self.show_error('Invalid Input', 'Please enter valid port numbers')
        
        add_btn = Button(text='Add', on_release=add_connection)
        cancel_btn = Button(text='Cancel', on_release=popup.dismiss)
        
        buttons.add_widget(add_btn)
        buttons.add_widget(cancel_btn)
        content.add_widget(buttons)
        
        popup.open()
    
    def toggle_connection(self, connection_item):
        """Toggle a connection on/off"""
        if connection_item.status == 'stopped':
            # Start connection
            success = self.proxy.start_proxy(
                connection_item.serial,
                connection_item.local_port,
                connection_item.remote_port
            )
            
            if success:
                self.db.update_connection_status(connection_item.connection_id, 'active')
                connection_item.status = 'active'
            else:
                self.show_error('Error', 'Failed to start proxy connection')
        else:
            # Stop connection
            success = self.proxy.stop_proxy(
                connection_item.serial,
                connection_item.local_port
            )
            
            if success:
                self.db.update_connection_status(connection_item.connection_id, 'stopped')
                connection_item.status = 'stopped'
            else:
                self.show_error('Error', 'Failed to stop proxy connection')
    
    def check_connection_ip(self, connection_item):
        """Check IP for a connection"""
        # Get device IP
        device_ip = self.adb.get_device_ip(connection_item.serial)
        
        if device_ip:
            self.db.update_connection_status(
                connection_item.connection_id,
                connection_item.status,
                device_ip
            )
            connection_item.current_ip = device_ip
            self.show_info('IP Check', f'Device IP: {device_ip}')
        else:
            self.show_error('IP Check Failed', 'Could not retrieve device IP')
    
    def change_connection_ip(self, connection_item):
        """Change IP by toggling airplane mode"""
        def do_change():
            success = self.adb.toggle_airplane_mode(connection_item.serial)
            
            if success:
                # Check new IP
                Clock.schedule_once(lambda dt: self.check_connection_ip(connection_item), 1)
                Clock.schedule_once(lambda dt: self.show_info(
                    'IP Changed',
                    'Airplane mode toggled. IP should be changed.'
                ), 0)
            else:
                Clock.schedule_once(lambda dt: self.show_error(
                    'Error',
                    'Failed to toggle airplane mode'
                ), 0)
        
        # Run in background thread to not block UI
        import threading
        threading.Thread(target=do_change, daemon=True).start()
        
        self.show_info('Changing IP', 'Toggling airplane mode...')
    
    def refresh_all(self):
        """Refresh both devices and connections"""
        self.refresh_devices()
        self.refresh_connections()
    
    def show_error(self, title, message):
        """Show error popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.3)
        )
        
        close_btn = Button(text='Close', size_hint_y=None, height=40, on_release=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()
    
    def show_info(self, title, message):
        """Show info popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.3)
        )
        
        close_btn = Button(text='Close', size_hint_y=None, height=40, on_release=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()


class MobileProxyApp(App):
    """Main application class"""
    
    def build(self):
        self.title = 'Mobile Proxy Manager'
        return MainLayout()


if __name__ == '__main__':
    # Check if CLI mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Remove the --cli argument and pass remaining args to cli
        sys.argv.pop(1)
        from cli import main as cli_main
        sys.exit(cli_main())
    else:
        # Run GUI mode
        MobileProxyApp().run()
