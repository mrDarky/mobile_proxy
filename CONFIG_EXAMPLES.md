# Mobile Proxy Manager - Example Configuration

# This file shows example configurations for different use cases

## Basic Setup - Single Device

# Device: Samsung Galaxy (Serial: R58M12345AB)
# Every Proxy listening on port: 8080
# Local port on computer: 9090

Connection:
  Device: R58M12345AB
  Local Port: 9090
  Remote Port: 8080
  
Usage:
  Configure your browser/app to use:
  - Host: 127.0.0.1 (or localhost)
  - Port: 9090
  - Type: HTTP/HTTPS

---

## Multi-Device Setup

# Device 1: Samsung Galaxy
Device 1:
  Serial: R58M12345AB
  Local Port: 9090
  Remote Port: 8080

# Device 2: Google Pixel
Device 2:
  Serial: 1A2B3C4D5E6F
  Local Port: 9091
  Remote Port: 8080

# Device 3: OnePlus
Device 3:
  Serial: ABC123XYZ789
  Local Port: 9092
  Remote Port: 8080

Usage:
  Browser 1 -> localhost:9090 (uses Device 1)
  Browser 2 -> localhost:9091 (uses Device 2)
  Browser 3 -> localhost:9092 (uses Device 3)

---

## Multiple Connections per Device

# Device: Samsung Galaxy (Serial: R58M12345AB)
# Multiple proxy apps or ports

Connection 1 (HTTP Proxy):
  Device: R58M12345AB
  Local Port: 9090
  Remote Port: 8080
  
Connection 2 (SOCKS5 Proxy):
  Device: R58M12345AB
  Local Port: 9091
  Remote Port: 1080

Connection 3 (Alternative Port):
  Device: R58M12345AB
  Local Port: 9092
  Remote Port: 8888

---

## Port Ranges for Organization

# Antidetect Browsers (9000-9009)
Browser Profile 1: localhost:9000
Browser Profile 2: localhost:9001
Browser Profile 3: localhost:9002

# Automation Scripts (9010-9019)
Script 1: localhost:9010
Script 2: localhost:9011
Script 3: localhost:9012

# Testing (9020-9029)
Test Environment 1: localhost:9020
Test Environment 2: localhost:9021

---

## Every Proxy App Configuration

Default Settings:
  - Port: 8080
  - Type: HTTP/HTTPS
  - Authentication: None (or configure if needed)

Alternative Settings:
  - Port: 8888
  - Type: SOCKS5
  - Port: 1080

Note: Make sure Every Proxy is running and configured
      before starting connections in Mobile Proxy Manager

---

## CLI Usage Examples

# List connected devices
python cli.py list-devices

# Add connection for device
python cli.py add R58M12345AB 9090 8080

# Start connection (ID 1)
python cli.py start 1

# Check device IP
python cli.py check-ip R58M12345AB

# Change device IP (toggle airplane mode)
python cli.py change-ip R58M12345AB

# Stop connection
python cli.py stop 1

# List all connections
python cli.py list-connections

---

## Common Port Numbers

Standard Ports:
  - 8080: Common HTTP proxy port
  - 1080: SOCKS proxy port
  - 8888: Alternative HTTP proxy port
  - 3128: Squid proxy default port

Local Ports (your choice):
  - 9090-9999: Recommended range for local connections
  - Avoid: 80, 443, 22, 3306, 5432 (system services)

---

## Troubleshooting Configuration

If Connection Fails:
  1. Verify Every Proxy is running on device
  2. Check remote port matches Every Proxy port
  3. Ensure local port is not already in use
  4. Check USB debugging is enabled
  5. Try different USB cable or port

If IP Check Fails:
  1. Ensure device is connected to WiFi or mobile data
  2. Check network permissions on device
  3. Try manual IP check in device settings

If IP Change Fails:
  1. Some devices require root for airplane mode control
  2. Try manual airplane mode toggle
  3. Check device permissions for automation
  4. Consider using WiFi reconnection as alternative
