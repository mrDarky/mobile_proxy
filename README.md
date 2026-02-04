# Mobile Proxy Manager

A cross-platform application built with Python and Kivy for creating proxy connections from mobile devices connected via USB.

## Features

- **Device Detection**: Automatically detect Android devices connected via USB using ADB
- **Multi-Device Support**: Connect and manage multiple phones simultaneously
- **Port Forwarding**: Create bridge connections from localhost:port to mobile:port
- **IP Management**: 
  - Check IP address for each connection
  - Change IP by toggling airplane mode on the device
- **Multiple Connections**: Create multiple proxy connections per device
- **SQLite Database**: Store device and connection configurations
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Android Debug Bridge (ADB)** installed and available in PATH
   - Windows: Download from [Android Platform Tools](https://developer.android.com/studio/releases/platform-tools)
   - macOS: `brew install android-platform-tools`
   - Linux: `sudo apt-get install android-tools-adb`
3. **USB Debugging** enabled on your Android device
4. **Every Proxy** app installed on your Android device (for proxy functionality)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/mrDarky/mobile_proxy.git
cd mobile_proxy
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Connect your Android device(s)** via USB and ensure USB debugging is enabled

2. **Run the application**:
```bash
python main.py
```

3. **Using the application**:
   - Click **"Refresh Devices"** to detect connected devices
   - Click **"Add Connection"** on a device to create a new proxy connection
   - Enter the local port (on your computer) and remote port (on the phone)
   - Click **"Start"** to activate the connection
   - Use **"Check IP"** to verify the device's current IP address
   - Use **"Change IP"** to toggle airplane mode and change the IP address

## Setting up Every Proxy on Android

1. Install **Every Proxy** from Google Play Store on your Android device
2. Configure the proxy settings in Every Proxy (e.g., listening on port 8080)
3. In Mobile Proxy Manager, create a connection with:
   - Local port: any available port (e.g., 9090)
   - Remote port: the port Every Proxy is listening on (e.g., 8080)
4. Start the connection
5. Configure your antidetect browser to use `localhost:9090` as the proxy

## Use Cases

- **Antidetect Browsers**: Use mobile IPs for browsing with antidetect browsers
- **Testing**: Test websites and applications from different mobile IPs
- **Automation**: Automate tasks that require rotating mobile IPs
- **Development**: Debug mobile applications with proxy interception

## Project Structure

```
mobile_proxy/
├── main.py              # Main application entry point
├── main.kv              # Kivy UI layout file
├── database.py          # SQLite database management
├── adb_manager.py       # ADB device management
├── proxy_manager.py     # Proxy connection handling
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Troubleshooting

### ADB Not Found
- Ensure ADB is installed and added to your system PATH
- Test by running `adb devices` in terminal

### Device Not Detected
- Enable USB debugging in Developer Options on your Android device
- Accept the USB debugging prompt on your device
- Try different USB cables or ports

### Connection Failed
- Ensure the remote port matches the port Every Proxy is listening on
- Check that Every Proxy is running on your device
- Verify no firewall is blocking the connection

### IP Change Not Working
- Ensure your app has permission to toggle airplane mode
- Some devices may require root access for airplane mode control
- Alternatively, manually toggle airplane mode on the device

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.