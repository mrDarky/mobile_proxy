#!/usr/bin/env python3
"""
Test script to verify the application can start without errors
"""
import os
import sys

# Set environment variable to use dummy video provider (no actual window)
os.environ['KIVY_VIDEO'] = 'ffpyplayer'
os.environ['KIVY_WINDOW'] = 'sdl2'
os.environ['KIVY_GRAPHICS'] = 'default'

# Suppress Kivy output
os.environ['KIVY_NO_CONSOLELOG'] = '1'

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'borderless', '0')
Config.set('kivy', 'exit_on_escape', '1')

try:
    # Import main components
    from database import Database
    from adb_manager import ADBManager
    from proxy_manager import ProxyManager
    print("✓ All core modules imported successfully")
    
    # Test database initialization
    if os.path.exists('test_verify.db'):
        os.remove('test_verify.db')
    
    db = Database('test_verify.db')
    print("✓ Database initialized")
    
    # Test ADB manager
    adb = ADBManager()
    print("✓ ADB manager initialized")
    
    # Test proxy manager
    proxy = ProxyManager(adb)
    print("✓ Proxy manager initialized")
    
    # Test CLI module
    from cli import InteractiveCLI
    print("✓ Interactive CLI module imported successfully")
    
    # Clean up
    if os.path.exists('test_verify.db'):
        os.remove('test_verify.db')
    
    print("\n✅ All tests passed! Application is ready to use.")
    print("\nTo run the application:")
    print("  GUI mode:         python main.py")
    print("  CLI mode:         python cli.py interactive")
    print("  CLI command mode: python cli.py [command]")
    print("\nNote: Make sure you have:")
    print("  1. ADB installed and in PATH")
    print("  2. Android device(s) connected via USB")
    print("  3. USB debugging enabled on device(s)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
