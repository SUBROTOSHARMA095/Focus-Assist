# Focus Assist

Focus Assist is a lightweight Python utility that monitors distracting applications running on your PC and automatically closes them when they exceed a preset usage limit. It helps reduce distractions by tracking app usage time and temporarily blocking apps that exceed the allowed time.

## Features

- Monitors selected distracting apps in real time
- Tracks how long an app has been running
- Terminates apps that exceed the configured usage limit
- Applies a cooldown period to prevent immediate relaunches
- Logs app usage time into a CSV file named `screen_time.csv`
- Runs in a loop until you stop it with `Ctrl+C`

## Supported apps

The script currently monitors these applications by default:

- `WhatsApp.exe`
- `brave.exe`

You can modify the `DISTRACTING_APPS` list in the script to add or remove apps.

## How it works

1. The script checks running processes using `psutil`.
2. If a monitored app starts, it begins tracking its runtime.
3. If the app stays open longer than the configured limit (`TIME_LIMIT`), it is terminated.
4. After termination, the app enters a cooldown period (`COOLDOWN_PERIOD`) before it can be relaunched.
5. The app name and total time spent are saved to `screen_time.csv`.

## Configuration

At the top of `focus assist.py`, you can adjust the following values:

```python
DISTRACTING_APPS = ["WhatsApp.exe", "brave.exe"]
TIME_LIMIT = 60
COOLDOWN_PERIOD = 30
GRACE_PERIOD = 5
```

### Explanation

- `DISTRACTING_APPS`: apps to monitor
- `TIME_LIMIT`: number of seconds an app may run before being blocked
- `COOLDOWN_PERIOD`: time before the app may restart after being blocked
- `GRACE_PERIOD`: brief delay used before forcefully terminating an app if needed

## Installation

1. Clone the repository:

```bash
git clone https://github.com/SUBROTOSHARMA095/Focus-Assist.git
cd Focus-Assist
```

2. Install dependencies:

```bash
pip install psutil
```

## Usage

Run the script:

```bash
python "focus assist.py"
```

The app will keep running in the terminal and monitor the configured distracting apps until you stop it with `Ctrl+C`.

## Output

The script creates or appends to a file named `screen_time.csv` in the project directory. It stores entries in the following format:

```csv
App Name,Time Spent (Seconds)
WhatsApp.exe,72
```

## Notes

- This project is intended for Windows-based app monitoring because it checks for `.exe` processes.
- Use this responsibly and only for apps you intentionally want to limit.
- The script may need to be run with administrator privileges depending on your system and the apps being managed.
  

## Project status

This is a simple standalone utility focused on distraction control and productivity. It is easy to customize for your own workflow and preferred apps.
