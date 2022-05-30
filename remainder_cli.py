import json
from socket import timeout
import time
from plyer import notification
from simple_term_menu import TerminalMenu

Reminders = {}
f = open('cache.json')
Reminders_created = json.load(f)
def show_term_menu():
    options = ["Add reminder", "Remove reminder", "show reminders"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f'You have selected:{options[menu_entry_index]}!')

    if options[menu_entry_index] == "Add reminder":
        rem_name = str(input("Name of your reminder: "))
        rem_description = str(input("Your reminders description: "))
        rem_time = float(input("Time:"))
        add_reminder(rem_name, rem_time, rem_description)

    elif options[menu_entry_index] == "show reminders":
        print(Reminders_created)


def show_reminders(local_time_assigned, name, description):
    local_time = local_time_assigned 
    time.sleep(local_time)
    notification.notify(title=name, message=description, timeout=5, app_name="Reminder", app_icon=r'./images/favicon.ico')


    
def add_reminder(name, time, description):
    Reminders[name] = ({'time': time, 'description': description})
    with open('cache.json', 'w') as f:
        json.dump(Reminders, f)
    show_reminders(time, name, description)

if __name__ == '__main__':
    show_term_menu()

f.close()