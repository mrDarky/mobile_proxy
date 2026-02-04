# Mobile Proxy Manager - Quick Reference

## Installation
```bash
pip install -r requirements.txt
```

## Prerequisites
- Python 3.7+
- ADB installed and in PATH
- Android device with USB debugging enabled
- Every Proxy app running on Android device

## Quick Start

### GUI Mode
```bash
python main.py
```

### CLI Mode
```bash
# List devices
python cli.py list-devices

# List connections
python cli.py list-connections

# Add connection
python cli.py add SERIAL_NUMBER LOCAL_PORT REMOTE_PORT

# Start connection
python cli.py start CONNECTION_ID

# Stop connection
python cli.py stop CONNECTION_ID

# Check IP
python cli.py check-ip SERIAL_NUMBER

# Change IP
python cli.py change-ip SERIAL_NUMBER
```

## Common Operations

### Add First Connection
1. Connect Android device via USB
2. Open Mobile Proxy Manager
3. Click "Refresh Devices"
4. Click "Add Connection" on your device
5. Enter: Local Port: 9090, Remote Port: 8080
6. Click "Add"

### Start Using Proxy
1. Click "Start" on the connection
2. Configure your browser/app:
   - Proxy: localhost or 127.0.0.1
   - Port: 9090 (your local port)
   - Type: HTTP/HTTPS

### Change IP
1. Click "Change IP" button
2. Wait 10-15 seconds
3. Click "Check IP" to verify new IP

## Troubleshooting

### ADB Not Found
```bash
# Test ADB installation
adb version

# If not installed:
# Windows: Download from developer.android.com
# macOS: brew install android-platform-tools
# Linux: sudo apt-get install android-tools-adb
```

### Device Not Detected
1. Enable Developer Options (tap Build Number 7 times)
2. Enable USB Debugging in Developer Options
3. Connect device and accept USB debugging prompt
4. Test: `adb devices`

### Connection Fails
1. Check Every Proxy is running on device
2. Verify remote port matches Every Proxy port
3. Try different local port if in use
4. Check firewall settings

## Port Recommendations

### Local Ports (Your Computer)
- Use range: 9000-9999
- Avoid: 80, 443, 22, 3306, 5432

### Remote Ports (Android Device)
- Default Every Proxy: 8080
- Alternative: 8888, 1080
- Check Every Proxy settings

## Example Configurations

### Single Device
```
Device: Samsung Galaxy (ABC123)
Connection: localhost:9090 → device:8080
Browser: 127.0.0.1:9090
```

### Multiple Devices
```
Device 1: localhost:9090 → device1:8080
Device 2: localhost:9091 → device2:8080
Device 3: localhost:9092 → device3:8080
```

### Multiple Connections per Device
```
Device 1: 
  - localhost:9090 → device:8080 (HTTP)
  - localhost:9091 → device:1080 (SOCKS5)
  - localhost:9092 → device:8888 (Alternative)
```

## Files

| File | Purpose |
|------|---------|
| main.py | GUI application |
| cli.py | CLI tool |
| database.py | Database management |
| adb_manager.py | ADB operations |
| proxy_manager.py | Proxy handling |
| main.kv | UI layout |
| README.md | Main documentation |
| USER_GUIDE.md | Complete user manual |
| CONFIG_EXAMPLES.md | Configuration examples |

## Keyboard Shortcuts (GUI)

- Escape: Exit application
- F5 (or Refresh): Refresh devices and connections

## Support

- Documentation: README.md, USER_GUIDE.md
- Examples: CONFIG_EXAMPLES.md
- Technical: IMPLEMENTATION_SUMMARY.md
- Issues: GitHub Issues

## License

MIT License - See LICENSE file
