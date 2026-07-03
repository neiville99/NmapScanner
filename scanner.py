import subprocess

from config import SCAN_TARGET
from db import create_db, save_scan_records
from parser import parse_nmap_xml

def check_nmap_installed() -> bool:
    try:
        result = subprocess.run(
            ["nmap", "--version"],
            capture_output=True,
            text=True,
            check=True
        )

        print("Nmap found")
        print(result.stdout.splitlines()[0])

        return True

    except FileNotFoundError:
        print("Nmap not found")
        print("Make sure Nmap installed")
        return False

    except subprocess.CalledProcessError as error:
        print("Nmap produced an error.")
        print(error.stderr)
        return False


def run_scan() -> str | None:
    if not check_nmap_installed():
        return None

    print(f"Starting scan for {SCAN_TARGET}")

    command = [
        "nmap",
        "-sV",
        "--version-light",
        "-T3",
        "-oX",
        "-",
        SCAN_TARGET
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        print("Scan completed")

        records = parse_nmap_xml(result.stdout)
        for record in records:
            print(record)

        save_scan_records(SCAN_TARGET, records)

        print("Scan saved")

        return records

    except subprocess.CalledProcessError as error:
        print("Scan failed")

        if error.stderr:
            print(error.stderr)

        if error.stdout:
            print(error.stdout)

        return None


if __name__ == "__main__":
    create_db()
    run_scan()