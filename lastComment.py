# adds to the table in input a "last comment" column with...
# the last comment

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
