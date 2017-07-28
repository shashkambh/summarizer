import json
import datetime
import argparse
import httplib2

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def urgent_task_filter(tasks):
    return [task for task in tasks if task['in_history'] == 1 and
        (task['priority'] == 4 or _is_today_or_later(task.date_string))]

def format_time(delta):
    mins, secs = divmod(delta.total_seconds(), 60)
    hrs, mins = divmod(mins, 60)
    secs = str(int(secs))
    mins = str(int(mins))
    hrs = str(int(hrs))
    return hrs + ' hours ' + mins + ' minutes ' + secs + ' seconds'

def get_today_bounds():
    prev_midnight = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    next_midnight = prevmidnight + datetime.timedelta(days=1)

    diff = datetime.datetime.utcnow() - datetime.datetime.now()
    prev_midnight = (prev_midnight + diff).isoformat() + 'Z'
    next_midnight = (next_midnight + diff).isoformat() + 'Z'
    return (prev_midnight, next_midnight)


def write_settings(className, data):
    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)

    settings[className] = data
    with open('settings.json', 'w') as settings_file:
        json.dump(settings, settings_file)

def get_oauth_connection(fileName):
    store = Storage(fileName)
    credentials = store.get()
    scopes = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar']

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        flow.user_agent = 'Query CLI'
        credentials = tools.run_flow(flow, store, flags)

    return credentials.authorize(httplib2.Http())
        

def _is_today_or_later(date_str):
    date_str = ' '.join(date_str.split()[:4])
    date = datetime.datetime.strptime(date_str, '%a %d %b %Y').date()
    today = datetime.date.today()
    return today <= date

