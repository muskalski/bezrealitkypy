# bezrealitky.py
bezrealitky.py - scrape bezrealitky website for new flat offers, translate their descriptions, get notified about the new offers by email - act quickly before somebody rents the place before you.
## Description
bezrealitky.py is basically scraping the bezrealitky website using criteria that you specify in the config file and create a single database file on a host machine with the info that you are interested in e.g. translated descriptions. And then send you an email with every newly appeared offers (database is used to track and persist the available offers). If you leave this running on your local or deploy somewhere to be run it’s gonna send you an email every time something new pops up in bezrealitky so you can act quickly before other 100 people see it and message the owner of the flat. Please use it reasonably :)
## Requirements
Create mailjet account https://www.mailjet.com/ to get api key and api secret
## Installation
Set up the config.ini file. Then run the following commands:
```
python3 -m venv .venv
pip3 install -r reqs.txt
python3 bezrealitky.py
```
