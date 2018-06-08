#########################
######## Imports ########
#########################

import sys
import json
import requests
import time
import datetime

#########################
### Global Variables ####
#########################

commands = ['start', 'stop', 'current', 'projects']

headers = {
    'Content-Type': 'application/json',
}

params = (
    ('with_related_data', 'true'),
)

#########################
### Helper Functions ####
#########################

def getAuthToken():
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    auth_token = (credentials['api_token'], "api_token")
    return auth_token

def getCurrentJSON(auth_token):
    # GET Request
    return requests.get('https://www.toggl.com/api/v8/time_entries/current',
                        auth=auth_token).json()['data']

def getProjectsJSON(auth_token):
    # GET Request
    return requests.get('https://www.toggl.com/api/v8/me',
                        params=params,
                        auth=auth_token).json()['data']['projects']

def parseTime(seconds):
    dt = datetime.timedelta(seconds=seconds)
    return str(dt).split(".")[0]

#########################
### Command Functions ###
#########################

def togglStop(auth_token, printResponse = True):
    # Get Current Timer
    current = getCurrentJSON(auth_token)

    # No Timer Running
    if current == None:
        if printResponse: print("No Ongoing Timer")
        return;
    current_id = str(current['id'])

    # PUT request
    response = requests.put('https://www.toggl.com/api/v8/time_entries/' + current_id + '/stop',
                            headers=headers,
                            auth=auth_token)
    if printResponse: print("Stopped Ongoing Timer")

def togglStart(auth_token):
    # Stop Any Ongoing Timers
    togglStop(auth_token, False)

    # Get Project Name
    projects = getProjectsJSON(auth_token)
    project = raw_input("Enter project: ")

    # Find Project ID
    found = False
    for p in projects:
        if p['name'] == project:
            found = True
            project_id = p['id']
            break
    if not found:
        print("Invalid Project")
        return

    # Get Description
    des = raw_input("Enter description: ")

    # Instantiate Data
    time_entry = dict()
    time_entry['description'] = des
    time_entry['pid'] = project_id
    time_entry['start'] = datetime.datetime.now().isoformat()
    time_entry['duration'] = -1 * time.time()
    time_entry['created_with'] = 'toggl_terminal'

    wrapper = dict()
    wrapper['time_entry'] = time_entry

    data = json.dumps(wrapper)

    # POST Request
    response = requests.post('https://www.toggl.com/api/v8/time_entries/start',
                             headers=headers,
                             data=data,
                             auth=auth_token).json()

def togglCurrent(auth_token):
    # Get Current Timer
    current = getCurrentJSON(auth_token)

    # No Timer Running
    if current == None:
        print("No Ongoing Timer")
        return

    # Project Details
    project_id = current['pid']
    des = current['description']
    duration = parseTime(current['duration'] + time.time())

    # Find Project Name
    projects = getProjectsJSON(auth_token)
    for p in projects:
        if p['id'] == project_id:
            project_name = p['name']
            break

    print("Ongoing Timer")
    print("Project: " + project_name)
    print("Description: " + des)
    print("Duration: " + duration)

def togglProjects(auth_token):
    # Get All Projects
    projects = getProjectsJSON(auth_token)
    result = []

    # Find Project ID
    for p in projects:
        result.append(str(p['name']))

    print(result)

#########################
##### Main Function #####
#########################

def main():
    # Get Command from Command Line
    if (len(sys.argv) != 2) or (sys.argv[1] not in commands):
        print("Invalid Argument")
        return
    else:
        command = sys.argv[1]

    # Get auth_token
    auth_token = getAuthToken()

    # Execute Command
    if command == 'stop':
        togglStop(auth_token)
    elif command == 'start':
        togglStart(auth_token)
    elif command == 'current':
        togglCurrent(auth_token)
    elif command == 'projects':
        togglProjects(auth_token)

if __name__ == '__main__':
    main()
