#!/usr/bin/env python3
# Search https://tgftp.nws.noaa.gov/data/raw/fl/flus41.kgyx.hwo.gyx.txt for the term "Weather spotters are encouraged to report"
import sys
import re
try:
    import requests
except ImportError:
    import os
    os.system('pip install requests')
    import requests
import os

STATUS_FILE = "last_status.txt" # Required to prevent spamming channels
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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" # Comment if not used
url = "https://tgftp.nws.noaa.gov/data/raw/fl/flus41.kgyx.hwo.gyx.txt" # Hazardous Weather Outlook URL

def read_last_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as file:
            return file.read().strip()
    return None

def write_last_status(status):
    with open(STATUS_FILE, "w") as file:
        file.write(status)

def post_to_slack(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

def main():
    # Load text from NWS Hazardous Weather Outlook URL
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raise an HTTPError for bad responses
        text = r.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        sys.exit(1)
    
    # Extract the report time
    time_match = re.search(r"\d{3,4} [AP]M [A-Z]{3} \w{3} \w{3} \d{1,2} \d{4}", text)
    report_time = time_match.group(0) if time_match else "Unknown time"
    
    match = re.search(r"Weather spotters are encouraged to report", text)
    current_status = "encouraged" if match else "not encouraged"
    
    last_status = read_last_status()
    
    if current_status != last_status:
        if current_status == "encouraged":
            message = f"Weather spotters are encouraged to report significant weather conditions according to Standard Operating Procedures. Last report: <{url}|{report_time}>."
        else:
            message = f"Weather spotters are not required at this time. Last report: <{url}|{report_time}>."
        
        if SLACK_WEBHOOK_URL:
            post_to_slack(message)
            print("Message sent to Slack.")
        
        # Output to console
        print(message)

        # Update the status file
        write_last_status(current_status)
    else:
        print(f"No change in status. Last report: <{url}|{report_time}>")
        exit

if __name__ == "__main__":
    main()