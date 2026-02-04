# Mobile Proxy Manager - User Guide

## Overview

Mobile Proxy Manager is a cross-platform desktop application that allows you to create proxy connections from your Android mobile devices to your computer. This enables you to use mobile IPs for browsing, testing, and automation tasks.

## How It Works

1. **Device Connection**: The app detects Android devices connected via USB using ADB (Android Debug Bridge)
2. **Port Forwarding**: Creates a bridge between a local port on your computer and a port on your mobile device
3. **Proxy Usage**: Your applications can connect to localhost:port which forwards traffic through the mobile device
4. **IP Management**: Check and change mobile IPs using airplane mode toggle

## Setup Guide

### Step 1: Install Prerequisites

#### Install ADB (Android Debug Bridge)

**Windows:**
1. Download Android Platform Tools from [developer.android.com](https://developer.android.com/studio/releases/platform-tools)
2. Extract the ZIP file to a folder (e.g., C:\platform-tools)
3. Add the folder to your system PATH:
   - Right-click "This PC" → Properties → Advanced System Settings
   - Click "Environment Variables"
   - Under System Variables, find "Path" and click Edit
   - Add the path to platform-tools folder
4. Open Command Prompt and verify: `adb version`

**macOS:**
```bash
brew install android-platform-tools
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install android-tools-adb
```

#### Install Python and Dependencies

1. Install Python 3.7 or higher from [python.org](https://www.python.org/downloads/)
2. Clone or download this repository
3. Open terminal in the project directory
4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Prepare Your Android Device

1. **Enable Developer Options:**
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
   - Developer Options will now appear in Settings

2. **Enable USB Debugging:**
   - Go to Settings → Developer Options
   - Enable "USB Debugging"

3. **Install Every Proxy:**
   - Download and install "Every Proxy" from Google Play Store
   - Open the app and configure it:
     - Enable proxy service
     - Note the port number (default is usually 8080)
     - Make sure it's running

4. **Connect to Computer:**
   - Connect your device via USB cable
   - When prompted on your device, allow USB debugging
   - Verify connection: Open terminal and run `adb devices`
   - You should see your device listed

### Step 3: Run the Application

1. Open terminal in the project directory
2. Run:
```bash
python main.py
```

3. The Mobile Proxy Manager window will open

## Using the Application

### Main Interface

The application window is divided into two main sections:

**Left Panel: Connected Devices**
- Shows all Android devices connected via USB
- Displays device model, serial number, and Android version
- "Add Connection" button to create new proxy connections

**Right Panel: Active Connections**
- Shows all configured proxy connections
- Displays status, ports, and IP information
- Control buttons for each connection

### Creating a Connection

1. Click "Refresh Devices" to detect connected devices
2. Find your device in the left panel
3. Click "Add Connection" button
4. Enter:
   - **Local Port**: Port on your computer (e.g., 9090)
   - **Remote Port**: Port where Every Proxy is listening (e.g., 8080)
5. Click "Add"

### Managing Connections

Each connection has three control buttons:

**Start/Stop:**
- Click "Start" to activate the connection
- Click "Stop" to deactivate it
- Green status = Active, Orange status = Stopped

**Check IP:**
- Checks and displays the device's current IP address
- Useful to verify the connection is working

**Change IP:**
- Toggles airplane mode on the device
- Forces the device to get a new IP address
- Takes about 10-15 seconds to complete

### Using the Proxy in Applications

Once a connection is active, configure your application to use:
- **Proxy Type**: HTTP/HTTPS or SOCKS5 (depends on Every Proxy configuration)
- **Host**: 127.0.0.1 or localhost
- **Port**: The local port you configured (e.g., 9090)

#### Example: Configure in Antidetect Browser

1. Open your antidetect browser settings
2. Navigate to proxy settings
3. Add new proxy:
   - Type: HTTP
   - Host: 127.0.0.1
   - Port: 9090 (your local port)
4. Test the connection
5. Start browsing with mobile IP

## Multiple Devices and Connections

### Multiple Devices
- Connect multiple phones via USB
- Each device appears in the left panel
- Create connections for each device

### Multiple Connections per Device
- You can create multiple connections to the same device
- Each connection uses different local ports
- Useful for different applications or parallel tasks

**Example Setup:**
- Device 1 → Connection 1: localhost:9090 → device:8080
- Device 1 → Connection 2: localhost:9091 → device:8081
- Device 2 → Connection 1: localhost:9092 → device:8080

## Troubleshooting

### "ADB Not Found" Error
- **Solution**: Install ADB and add it to your system PATH
- **Verify**: Run `adb version` in terminal
- **Restart** the application after installing ADB

### Device Not Appearing
- **Check USB Cable**: Use a data cable, not charge-only
- **Enable USB Debugging**: Settings → Developer Options → USB Debugging
- **Accept Prompt**: Check your device for "Allow USB debugging?" prompt
- **Try Different Port**: USB ports can sometimes cause issues
- **Verify ADB**: Run `adb devices` in terminal to see if device is listed

### Connection Fails to Start
- **Check Every Proxy**: Make sure it's running on your device
- **Verify Port**: Ensure the remote port matches Every Proxy's port
- **Port Conflict**: Local port might already be in use, try a different one
- **Firewall**: Check if firewall is blocking the connection

### "Change IP" Not Working
- **Permissions**: Some devices require root for airplane mode control
- **Manual Toggle**: Manually toggle airplane mode on your device
- **Alternative**: Use device settings to change network/reconnect WiFi

### IP Check Shows "Unknown"
- **WiFi Connection**: Device must be connected to WiFi
- **Permissions**: App might not have permission to read network info
- **Manual Check**: Go to device Settings → About Phone → Status → IP address

### Connection Drops Frequently
- **USB Cable**: Try a better quality cable
- **Power Saving**: Disable power saving mode on device
- **USB Debugging**: Keep USB debugging always enabled
- **Device Lock**: Some devices disable ADB when locked

## Advanced Usage

### Custom Port Ranges
- Use different port ranges for different purposes
- Example: 
  - 9000-9009 for browsing
  - 9010-9019 for automation
  - 9020-9029 for testing

### Rotating IPs
1. Create connection to device
2. Use it for a task
3. Click "Change IP" when needed
4. Wait 15 seconds for IP to change
5. Continue with new IP

### Batch Operations
- Connect multiple devices at once
- Create connections with sequential ports
- Use scripts to automate connection management

## Best Practices

1. **Label Your Devices**: Use device model to identify different phones
2. **Document Port Mappings**: Keep a note of which local port maps to which device
3. **Monitor Status**: Regularly check connection status and IPs
4. **Restart Connections**: If issues occur, stop and restart the connection
5. **Update Every Proxy**: Keep the Every Proxy app updated on your devices

## Security Considerations

1. **USB Debugging**: Only enable on trusted computers
2. **Network Security**: Be aware that traffic goes through your mobile network
3. **Data Usage**: Monitor your mobile data usage when using proxies
4. **Privacy**: Understand that your mobile carrier can see your traffic
5. **Permissions**: Review permissions granted to Every Proxy app

## Performance Tips

1. **USB 3.0**: Use USB 3.0 ports for better performance
2. **Close Unused**: Stop connections you're not actively using
3. **Limit Connections**: Too many active connections can slow down performance
4. **Good Signal**: Ensure devices have good mobile signal strength
5. **Power Management**: Keep devices charged during extended use

## Support

For issues, questions, or contributions:
- GitHub Issues: Submit bug reports and feature requests
- Documentation: Check README.md for technical details
- Community: Join discussions and share tips

## License

This project is licensed under the MIT License.
