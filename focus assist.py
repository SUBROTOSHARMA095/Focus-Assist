import psutil
import time
import csv

DISTRACTING_APPS = ["WhatsApp.exe", "brave.exe"]
TIME_LIMIT = 60
COOLDOWN_PERIOD = 30 
GRACE_PERIOD = 5 

def monitor_and_block_apps():
    print("Monitoring distracting apps... Press Ctrl+C to stop.")
    
    app_start_time = {}  
    cooldown_timers = {}

    with open("screen_time.csv", "a", newline="") as csvfile:
        fieldnames = ["App Name", "Time Spent (Seconds)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        try:
            while True:
                for process in psutil.process_iter(['pid', 'name']):
                    app_name = process.info['name']

                    if app_name in DISTRACTING_APPS:
                        if app_name in cooldown_timers and time.time() < cooldown_timers[app_name]:
                            print(f"{app_name} is in cooldown. Preventing restart.")
                            try:
                                proc = psutil.Process(process.info['pid'])
                                proc.terminate()
                            except psutil.NoSuchProcess:
                                pass
                            continue

                        if app_name not in app_start_time:
                            app_start_time[app_name] = time.time()
                            print(f"{app_name} started. Timer started.")

                        time_spent = time.time() - app_start_time[app_name]
                        
                        if time_spent > TIME_LIMIT:
                            print(f"{app_name} exceeded the time limit. Blocking the app gracefully...")
                            for proc in psutil.process_iter(['pid', 'name']):
                                if proc.info['name'] == app_name:
                                    try:
                                        process_instance = psutil.Process(proc.info['pid'])
                                        process_instance.terminate()  
                                        time.sleep(GRACE_PERIOD)  
                                        if process_instance.is_running():
                                            process_instance.kill() 
                                            print(f"{app_name} was forcefully terminated.")
                                        else:
                                            print(f"{app_name} closed gracefully.")
                                    except psutil.NoSuchProcess:
                                        print(f"{app_name} was already terminated.")

                            writer.writerow({"App Name": app_name, "Time Spent (Seconds)": int(time_spent)})

                            cooldown_timers[app_name] = time.time() + COOLDOWN_PERIOD

                            del app_start_time[app_name]

                for app_name in list(app_start_time.keys()):
                    if not any(process.info['name'] == app_name for process in psutil.process_iter(['name'])):
                        time_spent = time.time() - app_start_time[app_name]
                        print(f"{app_name} closed. Time spent: {int(time_spent)} seconds")
                        
                        writer.writerow({"App Name": app_name, "Time Spent (Seconds)": int(time_spent)})

                        del app_start_time[app_name]
                
                time.sleep(1) 
        except KeyboardInterrupt:
            print("Stopping app monitoring.")

if __name__ == "__main__":
    monitor_and_block_apps()
