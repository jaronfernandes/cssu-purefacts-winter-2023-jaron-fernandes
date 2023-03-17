"""Given a series of calendars please find the largest span of free time
available for everyone to meet between 9am and 5pm.
The meeting times are specified in a CSV file with the following format:
"""

import datetime
import csv
from typing import Optional


class Client:
    """
    client class
    """
    # start time, end time
    start_times: set
    end_times: set

    def __init__(self) -> None:
        """initializer"""
        self.start_times = set()
        self.end_times = set()

    def add_occupied_time(self, start_time: str, end_time: str) -> None:
        """add occupied time"""
        self.start_times.add(start_time)
        self.end_times.add(end_time)


"""
- have a list that goes from 9:00 to 5:00
- when calculating, make a list that checks if all clients are not in their occupied time. if ANY one of them are, do
NOT add a minute to the start time.
- if currently in a phase wehere you are trying to determine longest time, if you find a time that now a client is
occupied, then CAP that dict key off.
- store all times in dict. return the max start_time with the value. calculate end_time from there.
"""

filename = input('Please enter the file name: ')
print(filename)

clients = set()
available_times = {}
clients_available = {}

with open(filename) as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # skip the header row

    current_client = None

    for row in reader:
        if 'Client' in row[0]:
            if current_client is None:
                current_client = Client()
                clients.add(current_client)
                clients_available[row[0]] = (current_client, True)

        current_client.add_occupied_time(row[1], row[2])

# 9 - 10: 10-11. 11-12. 12-1. 1-2. 2-3. 3-4. 4-5.
# 60 * 8
current_start_time = None

for i in range(0, 60 * 8):
    hour = 9 + (i // 60)
    minute = i % 60

    if 0 <= minute <= 9:
        minute = '0' + str(minute)
    else:
        minute = str(minute)

    all_available = True
    # print(str(hour) + ':' + minute)

    for client in clients_available:
        if str(hour) + ':' + minute in clients_available[client][0].start_times:
            # print('hi')
            all_available = False
            clients_available[client] = (clients_available[client][0], False)

            if current_start_time is not None:
                current_start_time = None
            break

        elif clients_available[client][1] is False and str(hour) + ':' + minute not in \
                clients_available[client][0].end_times:
            # print('hi')
            all_available = False

            if current_start_time is not None:
                current_start_time = None
            break
        elif clients_available[client][1] is False and str(hour) + ':' + minute in \
                clients_available[client][0].end_times:
            clients_available[client] = (clients_available[client][0], True)

            continue
        else:
            continue
            # clients_available[client][1] == True and str(hour) + ':' + minute in
            # clients_available[client][0].start_times:

    # print(all_available)

    if all_available:
        if current_start_time is None:
            current_start_time = str(hour) + ':' + minute
            available_times[current_start_time] = 0

        available_times[current_start_time] += 1
        # print(available_times[current_start_time])

max_start_time = None

for times in available_times:
    if max_start_time is None or available_times[times] > available_times[max_start_time]:
        max_start_time = times

if max_start_time is None:
    print(None)
else:
    # print(available_times)

    print(max_start_time, f'{available_times[max_start_time]} minutes')
