# This script "closes" an initial list of issues under
# the operations of "subtasks, bloked by, requires, linked issues to this epic"
# it's not a tree because the links can point to any issue, so it's
# a proper graph visit.

from jira.client import JIRA
import csv
import sys
import time
import configurationData

reader = csv.reader(sys.stdin)

# a processed issue is an issue where all the
# "subtasks, bloked by, requires, linked issues to this epic"
# have been output in the list. Note that these outputted issues
# might not be "processedIssues" yet. This list only grows.
processedIssues = {}

# queue of issues to be processed. This list grows and shrinks.
issuesToBeProcessed = {}

# all issues that make to the list end up here. Not all these
# issues might be processedIssues yet. This list only grows.
listedIssues = {}
       
options = {
    'server': configurationData.jiraServerUrl
}

jira = JIRA(options, basic_auth=(configurationData.username, configurationData.password))    # a username/password tuple


fieldnames = ['issue id', 'why listed', 'summary']
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

rowNumber = 0
for row in csv.reader(iter(sys.stdin.readline, '')):
	rowNumber = rowNumber + 1
	# skip header
	if rowNumber > 1:

		key = row[0]
		# first, get the very issue itself. It's a query that will return only one issue.
		issues = jira.search_issues('id in (' + key + ')')
		for eachIssue in issues:
			if (not eachIssue.key in processedIssues) and (not eachIssue.key in listedIssues):
				issuesToBeProcessed[eachIssue.key] = 1
				listedIssues[eachIssue.key] = 1
				listedIssues[eachIssue.key] = 1
				writer.writerow({'issue id': eachIssue.key, 'why listed': 'in starting list: ' + key, 'summary': eachIssue.fields.summary})
				sys.stdout.flush()


while issuesToBeProcessed:
	sys.stderr.write('progress: ' + str(len(processedIssues)) + '/' + str(len(processedIssues) + len(issuesToBeProcessed)) + "\n")
	sys.stderr.write("\033[F") # Cursor up one line

	key = issuesToBeProcessed.popitem()[0]

	if key in processedIssues:
		continue


	issues = jira.search_issues('parent in (' + key + ')')
	for eachIssue in issues:
		#print ' > '+ eachIssue
		if (not eachIssue.key in processedIssues) and (not eachIssue.key in listedIssues):
			issuesToBeProcessed[eachIssue.key] = 1
			listedIssues[eachIssue.key] = 1
			writer.writerow({'issue id': eachIssue.key, 'why listed': 'child of: ' + key, 'summary': eachIssue.fields.summary})
			sys.stdout.flush()

	issues = jira.search_issues('"Epic Link" in (' + key + ')')
	for eachIssue in issues:
		#print ' > '+ eachIssue
		if (not eachIssue.key in processedIssues) and (not eachIssue.key in listedIssues):
			issuesToBeProcessed[eachIssue.key] = 1
			listedIssues[eachIssue.key] = 1
			writer.writerow({'issue id': eachIssue.key, 'why listed': 'linked to epic: ' + key, 'summary': eachIssue.fields.summary})
			sys.stdout.flush()

	issues = jira.search_issues('issue in linkedIssues(' + key + ',"requires")')
	for eachIssue in issues:
		#print ' > '+ eachIssue
		if (not eachIssue.key in processedIssues) and (not eachIssue.key in listedIssues):
			issuesToBeProcessed[eachIssue.key] = 1
			listedIssues[eachIssue.key] = 1
			writer.writerow({'issue id': eachIssue.key, 'why listed': 'required by: ' + key, 'summary': eachIssue.fields.summary})
			sys.stdout.flush()

	issues = jira.search_issues('issue in linkedIssues(' + key + ',"is blocked by")')
	for eachIssue in issues:
		#print ' > '+ eachIssue
		if (not eachIssue.key in processedIssues) and (not eachIssue.key in listedIssues):
			issuesToBeProcessed[eachIssue.key] = 1
			listedIssues[eachIssue.key] = 1
			writer.writerow({'issue id': eachIssue.key, 'why listed': 'blocks: ' + key, 'summary': eachIssue.fields.summary})
			sys.stdout.flush()


	processedIssues[key] = 1
	if key in issuesToBeProcessed:
		del issuesToBeProcessed[key]
