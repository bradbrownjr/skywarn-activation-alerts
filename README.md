# SKYWARN Activation Alerts
Ever wonder when the National Weather Service is looking for reports from SKYWARN spotters? Your local weather office may publish such a request in the *Hazardous Weather Outlook (HWO)* product, which is published to their website, to a public FTP site as a plaintext file, and is made available via their API. 

With these scripts, you can automatically search for the spotter request text, and alert your team that they are needed. The scripts check for the text "encouraged", as in 'Weather spotters are encouraged to report significant weather conditions according to Standard Operating Procedures.' If the keyword is present, it will indicate that spotters are needed.

# How do you find your HWO product?
Search for the local office by name or abbreviation, the product name, and the filetype.
Example: `gyx hwo filetype:txt`

The top result will look like this, and shouldn't change between storms:
https://tgftp.nws.noaa.gov/data/raw/fl/flus41.kgyx.hwo.gyx.txt

# Checking the HWO automatically
1. Save the raw Python file locally and mak it executable with `chmod +x skywarn-alert-wSlack.py`.
2. Add the HWO URL you found above to the `url=` variable
3. Create a cron job or scheduled task to run the script periodically, like hourly.

# Slack integration
To be documented. The short answer is, create a Slack app with an incoming webhook, and give it access to a channel in your workspace.

Vendor-provided information is found here:
https://api.slack.com/messaging/webhooks