import helpers
import time
import json
import requests
import imaplib
from datetime import datetime
from apiclient import discovery
from todoist.api import TodoistAPI

class Todoist:
    def __init__(self):
        with open('settings.json', 'r') as settings_file:
            # apiKey
            self.settings = json.load(settings_file)['todoist']

        self.api = TodoistAPI(self.settings['apiKey'])
        self.api.sync()

    def quick_add(self, task_string):
        self.api.quick.add(task_string)

    def get_all_tasks(self):
        return self.api['items']

    def get_urgent_tasks(self):
        return helpers.urgent_task_filter(self.get_all_tasks())

    def get_project_name(task):
        return self.api.projects.get(task['project_id'])

    def complete_task(self, task_name):
        matching_tasks = set()
        for task in self.get_all_tasks():
            if task_name in task['content']:
                matching_tasks.add(task)

        if len(matching_tasks) == 1:
            task = next(iter(matching_tasks))
            task.close()
            self.api.commit()
            return True

        print('ambiguous task')
        return False

    def print_task(self, task):
        project_name = self.api.projects.get_by_id(task['project_id'])['name']
        date = task['due_date_utc']
        if date is not None:
            date = ' '.join(task['due_date_utc'].split()[:4])

        print(
                str(date) + '\t' +
                str(project_name) + '\t' +
                str(task['content'])
             )

class Timer:
    def __init__(self):
        with open('settings.json', 'r') as settings_file:
            # timestamp?, description?
            self.settings = json.load(settings_file)['timer']

    def start(self, desc):
        current_time = datetime.now()
        self.settings['timestamp'] = time.mktime(current_time.timetuple())
        self.settings['description'] = desc
        helpers.write_settings('timer', self.settings)

    def current_timer(self):
        return self.settings['description']

    def stop(self):
        if not self.settings['timestamp'] or not self.settings['description']:
            print('No current timer')
            return

        desc = self.settings.pop('description')
        current_time = datetime.now()
        timestamp = self.settings.pop('timestamp')
        delta = current_time - datetime.fromtimestamp(timestamp)

        with open('time.log', 'a') as time_log_file:
            time_log_file.write(desc + ': ')
            time_log_file.write(helpers.format_time(delta) + '\n')

        helpers.write_settings('timer', self.settings)

class Gmail:
    def __init__(self):
        with open('settings.json', 'r') as settings_file:
            # storage_files: {email: file_name}
            self.settings = json.load(settings_file)['gmail']

        self.connections = {email: discovery.build('gmail', 'v1', helpers.get_oauth_connection(file_name)) for email, file_name in self.settings['storage_files'].items()}
    
    def get_num_unread(self):
        output = {}

        for email, conn in self.connections.items():
            service = discovery.build('gmail', 'v1', http=conn)
            
            response = service.users().messages().list(userId='me', q='is:unread').execute()
            num_messages = 0
            if 'messages' in response:
                num_messages += len(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId='me', q='is:unread', pageToken=page_token).execute()
                num_messages += len(response['messages'])

            output[email] = num_messages

        return output

class Calendar:
    def __init__(self):
        with open('settings.json', 'r') as settings_file:
            # storage_file
            self.settings = json.load(settings_file)['calendar']

        self.service = discovery.build('calendar', 'v3', helpers.get_oauth_connection(self.settings['storage_file']))

    def get_today_schedule(self):
        start, end = helpers.get_today_bounds()
        events_result = self.service.events().list(calendarId='primary', orderBy='startTime', timeMax=start, timeMin=end)
        return events_result.get('items', [])

    def add(self, event_text):
        self.service.events().quickAdd(calendarId='primary', text=event_text)

    def print_event(self, event):
        print(
                event['description'] + ' from ' + 
                event['start']['dateTime'].strftime('%H:%M') + ' to ' +
                event['end']['dateTime'].strftime('%H:%M')
             )


