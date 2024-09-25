import subprocess
import time
from datetime import datetime
import platform
import csv

def is_connected():
    try:
        # Adjust the ping command based on the operating system
        if platform.system().lower() == "windows":
            result = subprocess.run(["ping", "-n", "1", "google.com"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            result = subprocess.run(["ping", "-c", "1", "google.com"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        return result.returncode == 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def log_downtime(start, end):
    duration = end - start
    date_format = "%d-%m-%Y"
    time_format = "%I:%M:%S %p"

    date = start.strftime(date_format)
    start_time = start.strftime(time_format)
    end_time = end.strftime(time_format)
    formatted_duration = str(duration)

    with open("internet_downtime_log.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, start_time, end_time, formatted_duration])

def track_internet():
    downtime_start = None
    
    # Initialize the CSV file with headers if it does not exist
    with open("internet_downtime_log.csv", "a", newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Date", "Start Time", "End Time", "Duration"])
    
    while True:
        try:
            if is_connected():
                if downtime_start:
                    downtime_end = datetime.now()
                    log_downtime(downtime_start, downtime_end)
                    downtime_start = None
                print(f"{datetime.now()} - Internet is online")
            else:
                if not downtime_start:
                    downtime_start = datetime.now()
                print(f"{datetime.now()} - Internet is offline")
            
            # Wait for a while before pinging again
            time.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred in the tracking loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    while True:
        try:
            track_internet()
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)
