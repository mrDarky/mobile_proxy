# Mobile Proxy Manager - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                              │
├───────────────────────────────┬─────────────────────────────────────┤
│                               │                                     │
│    GUI (main.py + main.kv)    │      CLI (cli.py)                  │
│    • Kivy-based UI            │      • Command-line tool           │
│    • Real-time updates        │      • Automation support          │
│    • Interactive controls     │      • Scriptable                  │
│                               │                                     │
└───────────────────────────────┴─────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     CORE BUSINESS LOGIC                             │
├───────────────────────────────┬─────────────────────────────────────┤
│                               │                                     │
│  Proxy Manager                │  ADB Manager                       │
│  (proxy_manager.py)           │  (adb_manager.py)                  │
│  • Start/stop connections     │  • Device detection                │
│  • IP checking                │  • Port forwarding                 │
│  • Connection tracking        │  • Airplane mode toggle            │
│                               │  • Device properties               │
└───────────────────────────────┴─────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA PERSISTENCE                               │
├─────────────────────────────────────────────────────────────────────┤
│  Database (database.py)                                             │
│  • SQLite storage                                                   │
│  • Device management                                                │
│  • Connection configurations                                        │
│  • Status tracking                                                  │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SYSTEMS                                 │
├───────────────────────────┬─────────────────────────────────────────┤
│  ADB (Android Debug       │  Android Devices                       │
│  Bridge)                  │  • USB connection                      │
│  • Device communication   │  • Every Proxy app                     │
│  • Port forwarding        │  • Proxy services                      │
│  • Command execution      │                                        │
└───────────────────────────┴─────────────────────────────────────────┘
```

## Data Flow

### Connection Creation Flow
```
User → GUI/CLI → Database → Store Configuration
                          → Display Confirmation
```

### Start Connection Flow
```
User → GUI/CLI → Proxy Manager → ADB Manager → Device
                               → Create Port Forward
                ↓
             Database → Update Status
                ↓
             GUI/CLI → Display Success
```

### IP Check Flow
```
User → GUI/CLI → ADB Manager → Device
                             → Get IP Address
                ↓
             Database → Store IP
                ↓
             GUI/CLI → Display IP
```

### IP Change Flow
```
User → GUI/CLI → ADB Manager → Enable Airplane Mode (Device)
                             → Wait 5s
                             → Disable Airplane Mode (Device)
                             → Get New IP
                ↓
             Database → Update IP
                ↓
             GUI/CLI → Display New IP
```

## Component Responsibilities

### GUI (main.py + main.kv)
- Render user interface using Kivy
- Handle user interactions
- Display device and connection lists
- Show status updates and notifications
- Manage dialog boxes and popups

### CLI (cli.py)
- Parse command-line arguments
- Execute commands without GUI
- Provide feedback to terminal
- Enable automation and scripting

### Database (database.py)
- Manage SQLite database
- CRUD operations for devices and connections
- Store configuration persistently
- Track connection status and IPs

### ADB Manager (adb_manager.py)
- Communicate with ADB daemon
- Detect connected devices
- Create/remove port forwards
- Toggle airplane mode
- Retrieve device properties and IPs

### Proxy Manager (proxy_manager.py)
- Coordinate proxy operations
- Manage connection lifecycle
- Track active connections
- Check IP addresses

## Database Schema

### Devices Table
```sql
CREATE TABLE devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial_number TEXT UNIQUE NOT NULL,
    model TEXT,
    android_version TEXT,
    status TEXT DEFAULT 'connected',
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Connections Table
```sql
CREATE TABLE connections (
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
```

## Network Flow

### Proxy Traffic Flow
```
Application → localhost:9090 → ADB Port Forward → Device:8080 → Every Proxy → Internet
    ↓                                                                         ↑
    └─────────────────────────────────────────────────────────────────────────┘
```

### Detailed Network Path
1. Browser/App sends request to localhost:9090
2. ADB intercepts traffic on local port 9090
3. ADB forwards traffic through USB to device port 8080
4. Every Proxy app on device receives traffic
5. Every Proxy routes traffic through mobile network
6. Response follows reverse path

## Technology Stack

### Languages & Frameworks
- **Python 3.7+**: Core language
- **Kivy 2.3.0**: GUI framework
- **SQLite**: Database

### Libraries
- **adb-shell**: ADB communication
- **pure-python-adb**: Alternative ADB library
- **requests**: HTTP requests for IP checking
- **kivymd**: Material Design components

### External Tools
- **ADB**: Android Debug Bridge (system tool)
- **Every Proxy**: Android proxy app

## Design Patterns

### Separation of Concerns
- UI layer (GUI/CLI)
- Business logic layer (managers)
- Data layer (database)
- External integration layer (ADB)

### Single Responsibility
- Each module has one clear purpose
- Minimal coupling between modules
- Easy to test and maintain

### Error Handling
- Try-catch blocks for external operations
- User-friendly error messages
- Graceful degradation

## Scalability Considerations

### Current Limitations
- ADB connection is synchronous
- GUI updates on main thread
- Single-threaded operation

### Future Enhancements
- Async ADB operations
- Background thread for device monitoring
- Connection pooling
- Load balancing across devices
- Web interface with REST API

## Security Considerations

### Current Security
- Local-only operation
- ADB authentication required
- No network exposure
- Input validation on ports
- SQLite injection prevention

### Best Practices
- USB debugging should be enabled only when needed
- Connections should be stopped when not in use
- Monitor data usage on mobile devices
- Keep Every Proxy app updated

## Performance

### Optimizations
- SQLite indexing on serial_number and local_port
- Minimal UI updates
- Efficient ADB command execution
- Connection reuse

### Benchmarks
- Device detection: <1s
- Port forward creation: <0.5s
- IP check: 1-3s
- IP change: 10-15s (includes airplane mode toggle)

## Testing Strategy

### Unit Tests
- Database operations
- ADB command parsing
- Connection management

### Integration Tests
- Full workflow testing
- Multi-device scenarios
- Error handling

### Manual Testing
- UI interaction testing
- Real device testing
- Cross-platform verification

## Deployment

### Distribution
- Source code distribution via Git
- Python package installation via pip
- Platform-specific installers (future)

### Requirements
- Python 3.7+
- pip packages from requirements.txt
- ADB installed on system
- Android device with USB debugging

## Maintenance

### Code Quality
- PEP 8 style guidelines
- Comprehensive documentation
- Type hints (future enhancement)
- Regular updates

### Updates
- Bug fixes via GitHub
- Feature additions
- Security patches
- Documentation improvements
