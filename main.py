#! ./bin/python3
import sys
import apis

# command <appName> <taskType> <args>

def main():
    if len(sys.argv) == 1:
        print_summary()

    elif sys.argv[1] == 'task':
        todoist = apis.Todoist()
        if sys.argv[2] == 'add':
            todoist.quick_add(sys.argv[3])
        elif sys.argv[2] == 'finish':
            todoist.complete_task(sys.argv[3])
        elif sys.argv[2] == 'list':
            for task in todoist.get_all_tasks():
                todoist.print_task(task)
            
    elif sys.argv[1] == 'time':
        timer = apis.Timer()
        if sys.argv[2] == 'start':
            timer.start(sys.argv[3])
        if sys.argv[2] == 'stop':
            timer.stop()

    elif sys.argv[1] == 'mail':
        print('Not implemented!')

    elif sys.argv[1] == 'cal':
        calendar = apis.Calendar()
        if sys.argv[2] == 'add':
            calendar.add(sys.argv[3])
        elif sys.argv[2] == 'list':
            for event in calendar.get_today_schedule():
                calendar.print_event(event)

    elif sys.argv[1] == 'help':
        print('task {add finish list}')
        print('time {start stop}')
        print('cal {add list}')

def print_summary():
    todoist = apis.Todoist()
    for task in todoist.get_urgent_tasks():
        todoist.print_task(task)

    timer = apis.Timer()
    current_timer = timer.current_timer()
    if current_timer:
        print('Current timer is: ' + current_timer)

    mail = apis.Gmail()
    num_unread = mail.get_num_unread()
    for email, num in num_unread.items():
        print(num + ' unread messages in email ' + email)
    
    calendar = apis.Calendar()
    for event in calendar.get_today_schedule():
        calendar.print_event(event)

if __name__ == '__main__':
    main()
