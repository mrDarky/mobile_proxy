# CLI Interactive Mode - Menu Structure

This document shows the menu structure of the new CLI interactive mode.

## Main Menu
```
============================================================
  Mobile Proxy Manager - Main Menu
============================================================

  1. Devices Management
  2. Connections Management
  3. Quick Actions
  0. Exit

Enter choice:
```

## Devices Management Menu
```
============================================================
  Devices Management
============================================================

  1. List Connected Devices
  2. Refresh Device List
  3. Check Device IP
  4. Change Device IP
  5. View Device Details
  0. Back to Main Menu

Enter choice:
```

### Example: List Connected Devices
```
============================================================
  Connected Devices
============================================================

Found 2 device(s):

1. Samsung Galaxy S21 (R5CR20ABCDE)
   Android Version: 13

2. Google Pixel 6 (1A234B5C6D7E)
   Android Version: 14

Press Enter to continue...
```

## Connections Management Menu
```
============================================================
  Connections Management
============================================================

  1. List All Connections
  2. Add New Connection
  3. Start Connection
  4. Stop Connection
  5. Delete Connection
  6. View Connection Details
  0. Back to Main Menu

Enter choice:
```

### Example: List All Connections
```
============================================================
  All Connections
============================================================

Found 2 connection(s):

Connection ID: 1
  Device: R5CR20ABCDE
  Ports: localhost:9090 -> device:8080
  Status: active
  Current IP: 192.168.1.100
  Last Check: 2024-01-15 10:30:45

Connection ID: 2
  Device: 1A234B5C6D7E
  Ports: localhost:9091 -> device:8080
  Status: stopped
  Current IP: 192.168.1.101
  Last Check: 2024-01-15 09:15:22

Press Enter to continue...
```

### Example: Add New Connection
```
============================================================
  Add New Connection
============================================================

Available devices:
1. R5CR20ABCDE (Samsung Galaxy S21)
2. 1A234B5C6D7E (Google Pixel 6)

Enter device number (0 to cancel): 1
Enter local port (e.g., 9090): 9092
Enter remote port (e.g., 8080): 8080

✓ Connection added successfully (ID: 3)

Press Enter to continue...
```

## Quick Actions Menu
```
============================================================
  Quick Actions
============================================================

  1. Start All Connections
  2. Stop All Connections
  3. Check All IPs
  4. Show System Status
  0. Back to Main Menu

Enter choice:
```

### Example: Show System Status
```
============================================================
  System Status
============================================================

ADB Status: ✓ Available
Connected Devices: 2
Total Connections: 2
  Active: 1
  Stopped: 1

Press Enter to continue...
```

## Usage Instructions

### To run interactive mode:
```bash
python cli.py interactive
# or
python cli.py -i
# or
python main.py --cli interactive
```

### Navigation:
- Use number keys (0-9) to select menu options
- Press Enter to confirm your choice
- Use '0' to go back to the previous menu or exit
- The screen clears between menu transitions for a clean interface

### Features:
- **Devices Management**: Manage connected Android devices
- **Connections Management**: Create, start, stop, and delete proxy connections
- **Quick Actions**: Perform bulk operations on all connections
- **User-friendly**: Clear menus with descriptive options
- **No GUI required**: Works entirely in terminal/command prompt
