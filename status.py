# This script shows how to connect to a JIRA instance with a
# username and password over HTTP BASIC authentication.

from jira.client import JIRA
import csv
import sys
import time
import configurationData

reader = csv.reader(sys.stdin)
       
# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK.
# See
# https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK
# for details.

options = {
    'server': configurationData.jiraServerUrl
}

jira = JIRA(options, basic_auth=(configurationData.username, configurationData.password))    # a username/password tuple

# Get the mutable application properties for this server (requires
# jira-system-administrators permission)
props = jira.application_properties()

# Find all issues reported by the admin


rowNumber = 0
reader = csv.reader(iter(sys.stdin.readline, ''))
fieldnamesReceived = reader.next()
fieldnamesReceived.append('status')

writer = csv.DictWriter(sys.stdout, fieldnames=fieldnamesReceived)
writer.writeheader()

for row in reader:
	key = row[0]

	issues = jira.search_issues('id in (' + key + ')')


	for eachIssue in issues:

		rowToBeWritten = {}
		for x in range(0, len(fieldnamesReceived)):
			if fieldnamesReceived[x] != 'status':
				rowToBeWritten[fieldnamesReceived[x]] = row[x]
			rowToBeWritten['status'] = eachIssue.fields.status

		writer.writerow(rowToBeWritten)
		sys.stdout.flush()
