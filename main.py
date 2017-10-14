# -*- coding: utf-8 -*-
from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
from json import loads
import sys, traceback

def run():
    #Load credentials from local file '.gitlabCredentials'
    file = open('.redmineCredentials', 'r')
    credentials = loads(file.read())

    address = credentials['address']
    username = credentials['username']
    password = credentials['password']

    try:
        redmine = Redmine(address, username=username, password=password)
        #issues = redmine.issue.filter(status_id='*', sort='id')
        #ids = [ int(id) for id in issues ]
        #for id in ids:
        #    print(str(id))
        firstIssue = redmine.issue.get(1)
        #for prop in firstIssue:
        #    print(str(prop))
        print('"' + str(firstIssue.project) + '"[id=' + str(firstIssue.project.id) + ']=>"' + firstIssue.subject.encode('utf-8') + '"[id=' + str(firstIssue.id) + "]")
    except:
        print('Could not connect to "' + address + '"!')
        print('-'*60)
        traceback.print_exc(file=sys.stderr)
        return -1
    reachId = credentials['reachId']
    try:
        reachIssue = redmine.issue.get(reachId)
        print("Ticket exists!")
        try:
            goalIssue = redmine.issue.get(reachId + 1)
            print("Too late...")
        except:
            print("Creating new issue...")
            try:
                goalIssue = redmine.issue.create(
                    project_id=credentials['newIssue']['projectId'],
                    subject=credentials['newIssue']['subject'],
                    tracker_id=credentials['newIssue']['trackerId'],
                    description=credentials['newIssue']['description'],
                    status_id=credentials['newIssue']['statusId'],
                    priority_id=credentials['newIssue']['priorityId'],
                    assigned_to_id=credentials['newIssue']['assignedToId'])
                print("OK!")
            except:
                print("Could not create new ticket!!")
                print('-'*60)
                traceback.print_exc(file=sys.stderr)
                return -3
    except ResourceNotFoundError:
        print('Reach ticket does not yet exist. Doing nothing...')
    except:
        print("Unknown error occured!")
        print('-'*60)
        traceback.print_exc(file=sys.stderr)
        return -2

    return 0

if __name__ == '__main__':
    sys.exit(run())
