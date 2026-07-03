# NmapScanner
A python based network scanning project that runs Nmap scans, parses the xml output, and stores scan results in a local SQLite database. The project is designed to be automated using Windows Tasl Schedular

## Files
.env: Stores the scan target. Example: SCAN_TARGET=127.0.0.1
config.py: Loads the scan target from the .env file and checks that it is not empty.
db.py: Creates the SQLite database and saves scan records into the scans and scan_results tables.
parser.py: Reads the XML output from Nmap and turns it into Python dictionaries.
scanner.py: Main file. Checks that Nmap is installed, runs the scan, parses the results, and saves them to the database.
run_scan.bat: Windows batch file used to run scanner.py from Task Scheduler.
scans.db: SQLite database created by the program. This stores the scan history and scan result records.

## Requirements
Python: Install Python 3.10 or newer.
Nmap: Install Nmap and make sure it is added to the Windows PATH.
python-dotenv: Install this Python package so the project can read the .env file.

## Install Python Packages
Open Command Prompt inside the project folder and run:
```
pip install python-dotenv
```

## Set Up The .env File
Create a file called .env in the same folder as the Python files.

Add this line:

```
SCAN_TARGET="Target IP"
```

Use 127.0.0.1 to scan your own computer.
Only scan systems you own or have permission to test.

## Run The Scanner Manually
Open Command Prompt in the project folder and run:

```
python scanner.py
```
The program should check Nmap, run the scan, create the database, and save the results.

## Set Up The Batch File
Create a file called run_scan.bat in the project folder.
Add this:

```bat
@echo off
cd /d "%~dp0"
python scanner.py
```

If you are using a virtual environment, use this instead:

```bat
@echo off
cd /d "%~dp0"
.venv\Scripts\python.exe scanner.py
```

Save the file as ANSI or UTF-8 without BOM.

This avoids the error where Windows says @echo is not recognised.

## Test The Batch File

Double-click run_scan.bat.

The scanner should run and save results to scans.db.

You can also test it from Command Prompt:

```bat
cmd.exe /c run_scan.bat
```

## Set Up Windows Task Scheduler

Open Task Scheduler.

Click Create Basic Task.

Name it AutoNmap Scan.

Choose how often you want it to run, such as Daily.

Choose the time you want the scan to start.

Select Start a program.

For Program/script, choose your run_scan.bat file.

Finish the task setup.

## Check The Scheduled Task

Open Task Scheduler.

Go to Task Scheduler Library.

Find AutoNmap Scan.

Right-click it and choose Run.

Check the Last Run Result after it finishes.

## Important Notes

The Python files do not control the schedule.

Windows Task Scheduler controls when the scan runs.

The Python program only runs once each time it is started.

Do not share scans.db publicly if it contains real scan results.

Do not scan public IP addresses, company systems, or other devices without permission.
