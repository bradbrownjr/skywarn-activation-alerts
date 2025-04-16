#!/usr/bin/env python3
# Search https://tgftp.nws.noaa.gov/data/raw/fl/flus41.kgyx.hwo.gyx.txt for the term "Weather spotters are encouraged to report"
import sys
import re
import requests
import os

STATUS_FILE = "last_status.txt"

def read_last_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as file:
            return file.read().strip()
    return None

def write_last_status(status):
    with open(STATUS_FILE, "w") as file:
        file.write(status)

def main():
    url = "https://tgftp.nws.noaa.gov/data/raw/fl/flus41.kgyx.hwo.gyx.txt"
    r = requests.get(url)
    text = r.text
    
    # Extract the report time
    time_match = re.search(r"\d{3,4} [AP]M [A-Z]{3} \w{3} \w{3} \d{1,2} \d{4}", text)
    report_time = time_match.group(0) if time_match else "Unknown time"
    
    match = re.search(r"Weather spotters are encouraged to report", text)
    current_status = "encouraged" if match else "not encouraged"
    
    last_status = read_last_status()
    
    if current_status != last_status:
        if current_status == "encouraged":
            print(f"Weather spotters are encouraged to report, please refer to the Hazardous Weather Outlook for details. Last report time: {report_time}")
        else:
            print(f"Weather spotters are not encouraged to report at this time. Last report time: {report_time}")
        write_last_status(current_status)
    else:
        print(f"No change in status. Last report time: {report_time}") # Remark this line when we go live to avoid spamming

if __name__ == "__main__":
    main()