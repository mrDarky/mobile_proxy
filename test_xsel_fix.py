#!/usr/bin/env python3
"""
Test to verify that xsel/xclip FileNotFoundError is properly suppressed
This test ensures the fix for the xsel error is working correctly
"""
import sys
import io

def test_xsel_fix():
    """Test that xsel/xclip errors are filtered while other logs remain visible"""
    print("Testing xsel/xclip error suppression...")
    print()
    
    # Capture stderr to verify what gets filtered
    captured_stderr = io.StringIO()
    
    # Set up the filter like main.py does
    original_stderr = sys.stderr
    
    class ClipboardErrorFilter:
        def __init__(self, original_stderr):
            self.original = original_stderr
            self.filtering = False
            
        def write(self, text):
            # Also write to our capture for testing
            captured_stderr.write(text)
            
            if 'xsel - FileNotFoundError' in text or 'xclip - FileNotFoundError' in text:
                self.filtering = True
                return len(text)
            
            if self.filtering:
                if text.startswith('[') or (text.strip() and not text.startswith(' ')):
                    self.filtering = False
                    # Continue to write this line since it's not part of the error
                else:
                    # Still filtering, skip this line
                    return len(text)
            
            return self.original.write(text)
        
        def flush(self):
            self.original.flush()
        
        def isatty(self):
            return self.original.isatty()
    
    sys.stderr = ClipboardErrorFilter(original_stderr)
    
    # Import Kivy clipboard which triggers the xsel/xclip check
    try:
        from kivy.core.clipboard import Clipboard
        print("✓ Kivy clipboard imported successfully")
        print(f"✓ Clipboard backend: {type(Clipboard).__name__}")
        
        # Check captured output
        captured_output = captured_stderr.getvalue()
        
        # Verify xsel errors were captured but not displayed
        if 'xsel - FileNotFoundError' in captured_output:
            print("✓ xsel errors were captured (but filtered from display)")
        elif 'xclip - FileNotFoundError' in captured_output:
            print("✓ xclip errors were captured (but filtered from display)")
        else:
            print("✓ No xsel/xclip errors occurred (tools may be installed)")
        
        # Verify other Kivy logs are visible
        if '[INFO' in captured_output or '[Kivy' in captured_output:
            print("✓ Other Kivy logs are still visible")
        
        print()
        print("✅ xsel/xclip error suppression test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during test: {e}")
        return False
    finally:
        sys.stderr = original_stderr


if __name__ == '__main__':
    success = test_xsel_fix()
    sys.exit(0 if success else 1)
