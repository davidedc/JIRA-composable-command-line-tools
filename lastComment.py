# This script shows how to connect to a JIRA instance with a
# username and password over HTTP BASIC authentication.

from jira.client import JIRA
import csv
import sys
import time
import usernamePasswordData

reader = csv.reader(sys.stdin)
       
# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK.
# See
# https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK
# for details.

options = {
    'server': 'https://jira.shazamteam.net/'
}

jira = JIRA(options, basic_auth=(usernamePasswordData.username, usernamePasswordData.password))    # a username/password tuple

# Get the mutable application properties for this server (requires
# jira-system-administrators permission)
props = jira.application_properties()

# Find all issues reported by the admin


rowNumber = 0
reader = csv.reader(iter(sys.stdin.readline, ''))
fieldnamesReceived = reader.next()
fieldnamesReceived.append('last comment body')
fieldnamesReceived.append('last comment created')
fieldnamesReceived.append('last comment author')

writer = csv.DictWriter(sys.stdout, fieldnames=fieldnamesReceived)
writer.writeheader()

for row in reader:
	key = row[0]

	issue2ndStepCommentRetrieval = jira.issue(key, expand='comments')
	maxTime = 0
	maxTimeCommentBody = 'no comments'
	maxTimeCommentAuthor = 'no comments'
	for eachComment in issue2ndStepCommentRetrieval.fields.comment.comments:
		if eachComment.created > maxTime:
			maxTime = eachComment.created
			maxTimeCommentBody = eachComment.body
			maxTimeCommentAuthor = eachComment.author
	#sys.stderr.write("last comment created: " +  maxTime + ' ' + maxTimeComment + " \n");

	# first, get the very issue itself. It's a query that will return only one issue.
	time.sleep(1)
	issues = jira.search_issues('id in (' + key + ')')


	for eachIssue in issues:

		rowToBeWritten = {}
		for x in range(0, len(fieldnamesReceived)):
			if fieldnamesReceived[x] != 'last comment body' and fieldnamesReceived[x] != 'last comment created' and fieldnamesReceived[x] != 'last comment author':
				rowToBeWritten[fieldnamesReceived[x]] = row[x]
			rowToBeWritten['last comment body'] = maxTimeCommentBody
			rowToBeWritten['last comment created'] = maxTime
			rowToBeWritten['last comment author'] = maxTimeCommentAuthor

		writer.writerow(rowToBeWritten)
		sys.stdout.flush()
