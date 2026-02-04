import subprocess
import sys
import os
from datetime import datetime

def run_tests():
    print("=" * 80)
    print("SELENIUM TEST AUTOMATION FRAMEWORK")
    print("=" * 80)
    print()
    
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    cmd = ["pytest", "test_amazon.py", "-v", "-s"]
    
    if len(sys.argv) > 1 and sys.argv[1] == "-m":
        cmd.extend(["-m", sys.argv[2]])
        print(f"Running tests with marker: {sys.argv[2]}")
    else:
        print("Running all tests")
    
    print()
    print("=" * 80)
    print("EXECUTING TESTS...")
    print("=" * 80)
    print()
    
    result = subprocess.run(cmd)
    
    print()
    print("=" * 80)
    print("TEST EXECUTION COMPLETED")
    print("=" * 80)
    print()
    print("Generated artifacts:")
    print("  - Extent Report: reports/")
    print("  - Screenshots: screenshots/")
    print("  - Logs: logs/")
    print()
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)