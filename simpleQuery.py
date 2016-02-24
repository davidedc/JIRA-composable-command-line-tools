# takes the query in input and creates the resulting table

from jira.client import JIRA
import csv
import sys
import time
import configurationData

reader = csv.reader(sys.stdin)
processedIssues = {}
issuesToBeProcessed = {}
       
options = {
    'server': configurationData.jiraServerUrl
}

jira = JIRA(options, basic_auth=(configurationData.username, configurationData.password))    # a username/password tuple

fieldnames = ['issue id', 'summary']
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

rowNumber = 0
queryFromStdin = sys.stdin.readline()
#sys.stderr.write('query: ' + queryFromStdin)

issues = jira.search_issues(queryFromStdin)
for eachIssue in issues:
	summary_truncated = (eachIssue.fields.summary[:40] + '..') if len(eachIssue.fields.summary) > 40 else eachIssue.fields.summary
	writer.writerow({'issue id': eachIssue.key, 'summary': eachIssue.fields.summary})
	sys.stdout.flush()
