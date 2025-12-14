import subprocess
import sys

print("Running tests...")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_vacaciones.py", "-vv"],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    with open("test_results.log", "w", encoding="utf-8") as f:
        f.write("STDOUT:\n")
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
        
    print(f"Tests finished. Return code: {result.returncode}")
except Exception as e:
    print(f"Error running tests: {e}")
