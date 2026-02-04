#!/usr/bin/env python3
"""
Test the CLI interactive mode functionality
This verifies that all menu methods exist and are callable
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cli_interactive():
    """Test that InteractiveCLI can be instantiated and has all required methods"""
    from cli import InteractiveCLI
    
    print("Testing CLI Interactive Mode...")
    print()
    
    # Create instance (will fail if ADB is not available, but that's ok for structure test)
    try:
        cli = InteractiveCLI()
        print("✓ InteractiveCLI instantiated successfully")
    except Exception as e:
        print(f"✗ Failed to instantiate InteractiveCLI: {e}")
        return False
    
    # Check main methods
    required_methods = [
        'main_menu',
        'devices_menu',
        'connections_menu',
        'quick_actions_menu',
        'run',
        'clear_screen',
        'print_header',
        'print_menu',
        'get_input',
        'pause',
    ]
    
    print("\nChecking main menu methods:")
    for method in required_methods:
        if hasattr(cli, method) and callable(getattr(cli, method)):
            print(f"  ✓ {method}()")
        else:
            print(f"  ✗ {method}() not found")
            return False
    
    # Check device action methods
    device_methods = [
        'list_devices_action',
        'refresh_devices_action',
        'check_device_ip_action',
        'change_device_ip_action',
        'view_device_details_action',
    ]
    
    print("\nChecking device action methods:")
    for method in device_methods:
        if hasattr(cli, method) and callable(getattr(cli, method)):
            print(f"  ✓ {method}()")
        else:
            print(f"  ✗ {method}() not found")
            return False
    
    # Check connection action methods
    connection_methods = [
        'list_connections_action',
        'add_connection_action',
        'start_connection_action',
        'stop_connection_action',
        'delete_connection_action',
        'view_connection_details_action',
    ]
    
    print("\nChecking connection action methods:")
    for method in connection_methods:
        if hasattr(cli, method) and callable(getattr(cli, method)):
            print(f"  ✓ {method}()")
        else:
            print(f"  ✗ {method}() not found")
            return False
    
    # Check quick action methods
    quick_action_methods = [
        'start_all_connections_action',
        'stop_all_connections_action',
        'check_all_ips_action',
        'show_system_status_action',
    ]
    
    print("\nChecking quick action methods:")
    for method in quick_action_methods:
        if hasattr(cli, method) and callable(getattr(cli, method)):
            print(f"  ✓ {method}()")
        else:
            print(f"  ✗ {method}() not found")
            return False
    
    # Check that components are initialized
    print("\nChecking component initialization:")
    if hasattr(cli, 'db'):
        print("  ✓ Database initialized")
    else:
        print("  ✗ Database not initialized")
        return False
    
    if hasattr(cli, 'adb'):
        print("  ✓ ADB Manager initialized")
    else:
        print("  ✗ ADB Manager not initialized")
        return False
    
    if hasattr(cli, 'proxy'):
        print("  ✓ Proxy Manager initialized")
    else:
        print("  ✗ Proxy Manager not initialized")
        return False
    
    if hasattr(cli, 'running'):
        print("  ✓ Running flag initialized")
    else:
        print("  ✗ Running flag not initialized")
        return False
    
    return True

def test_cli_command_mode():
    """Test that CLI command mode still works"""
    import cli
    
    print("\n\nTesting CLI Command Mode...")
    print()
    
    functions = [
        'list_devices',
        'list_connections', 
        'add_connection',
        'start_connection',
        'stop_connection',
        'check_ip',
        'change_ip',
    ]
    
    for func_name in functions:
        if hasattr(cli, func_name) and callable(getattr(cli, func_name)):
            print(f"  ✓ {func_name}() function exists")
        else:
            print(f"  ✗ {func_name}() function not found")
            return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("  CLI Interactive Mode Tests")
    print("=" * 60)
    print()
    
    try:
        interactive_ok = test_cli_interactive()
        command_ok = test_cli_command_mode()
        
        print("\n" + "=" * 60)
        if interactive_ok and command_ok:
            print("✅ All tests passed!")
            print("\nThe CLI interactive mode is ready to use:")
            print("  python cli.py interactive")
            print("  python cli.py -i")
            print("\nThe CLI command mode is also available:")
            print("  python cli.py list-devices")
            print("  python cli.py list-connections")
            print("  etc.")
            return 0
        else:
            print("❌ Some tests failed!")
            return 1
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
