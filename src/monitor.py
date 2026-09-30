import subprocess
import sys


# --------------------------------------------------
# Automated Monitoring System
# --------------------------------------------------

def run_monitoring():

    print("\n===================================")
    print("      AI ANOMALY WATCHER")
    print("      AUTOMATED MONITORING")
    print("===================================")

    print("\nStarting anomaly detection...\n")

    # Run anomaly detection
    result = subprocess.run(
        [
            sys.executable,
            "src/anomaly_detector.py"
        ],
        capture_output=True,
        text=True
    )

    # Display output
    print(result.stdout)

    # Display errors if any
    if result.stderr:

        print("\nMonitoring Error:")
        print(result.stderr)

    print("\n===================================")
    print("      MONITORING COMPLETED")
    print("===================================")


# --------------------------------------------------
# Run monitoring
# --------------------------------------------------

if __name__ == "__main__":

    run_monitoring()