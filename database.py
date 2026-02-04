"""
Database module for managing device and connection configurations
"""
import sqlite3
import json
from datetime import datetime


class Database:
    def __init__(self, db_path='mobile_proxy.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Devices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number TEXT UNIQUE NOT NULL,
                model TEXT,
                android_version TEXT,
                status TEXT DEFAULT 'connected',
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Connections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                local_port INTEGER NOT NULL,
                remote_port INTEGER NOT NULL,
                status TEXT DEFAULT 'stopped',
                current_ip TEXT,
                last_check TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (device_id) REFERENCES devices (id),
                UNIQUE(local_port)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_device(self, serial_number, model='', android_version=''):
        """Add or update a device in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO devices (serial_number, model, android_version, last_seen)
            VALUES (?, ?, ?, ?)
        ''', (serial_number, model, android_version, datetime.now()))
        
        device_id = cursor.lastrowid
        if device_id == 0:  # Device already exists
            cursor.execute('SELECT id FROM devices WHERE serial_number = ?', (serial_number,))
            device_id = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        return device_id
    
    def get_devices(self):
        """Get all devices"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, serial_number, model, android_version, status, last_seen FROM devices')
        devices = cursor.fetchall()
        
        conn.close()
        return devices
    
    def add_connection(self, device_id, local_port, remote_port):
        """Add a new connection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO connections (device_id, local_port, remote_port, status)
                VALUES (?, ?, ?, 'stopped')
            ''', (device_id, local_port, remote_port))
            
            connection_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return connection_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def get_connections(self, device_id=None):
        """Get all connections, optionally filtered by device_id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if device_id:
            cursor.execute('''
                SELECT c.id, c.device_id, d.serial_number, c.local_port, c.remote_port, 
                       c.status, c.current_ip, c.last_check
                FROM connections c
                JOIN devices d ON c.device_id = d.id
                WHERE c.device_id = ?
            ''', (device_id,))
        else:
            cursor.execute('''
                SELECT c.id, c.device_id, d.serial_number, c.local_port, c.remote_port, 
                       c.status, c.current_ip, c.last_check
                FROM connections c
                JOIN devices d ON c.device_id = d.id
            ''')
        
        connections = cursor.fetchall()
        conn.close()
        return connections
    
    def update_connection_status(self, connection_id, status, ip=None):
        """Update connection status and IP"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if ip:
            cursor.execute('''
                UPDATE connections 
                SET status = ?, current_ip = ?, last_check = ?
                WHERE id = ?
            ''', (status, ip, datetime.now(), connection_id))
        else:
            cursor.execute('''
                UPDATE connections 
                SET status = ?
                WHERE id = ?
            ''', (status, connection_id))
        
        conn.commit()
        conn.close()
    
    def delete_connection(self, connection_id):
        """Delete a connection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM connections WHERE id = ?', (connection_id,))
        
        conn.commit()
        conn.close()
    
    def delete_device(self, device_id):
        """Delete a device and all its connections"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM connections WHERE device_id = ?', (device_id,))
        cursor.execute('DELETE FROM devices WHERE id = ?', (device_id,))
        
        conn.commit()
        conn.close()
