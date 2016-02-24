# takes the table passed as input and adds a "status" column
# with the status

from jira.client import JIRA
import csv
import sys
import time
import configurationData

reader = csv.reader(sys.stdin)
       
options = {
    'server': configurationData.jiraServerUrl
}

jira = JIRA(options, basic_auth=(configurationData.username, configurationData.password))    # a username/password tuple

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
