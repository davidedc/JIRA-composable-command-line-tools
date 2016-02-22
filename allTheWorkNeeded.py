# This script shows how to connect to a JIRA instance with a
# username and password over HTTP BASIC authentication.

from jira.client import JIRA
import csv
import sys
import time
import configurationData

reader = csv.reader(sys.stdin)
processedIssues = {}
issuesToBeProcessed = {}
       
# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK.
# See
# https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK
# for details.

options = {
    'server': 'https://jira.shazamteam.net/'
}

jira = JIRA(options, basic_auth=(configurationData.username, configurationData.password))    # a username/password tuple

# Get the mutable application properties for this server (requires
# jira-system-administrators permission)
props = jira.application_properties()

# Find all issues reported by the admin

fieldnames = ['issue id', 'why listed', 'summary']
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

rowNumber = 0
for row in csv.reader(iter(sys.stdin.readline, '')):
	rowNumber = rowNumber + 1
	# skip header
	if rowNumber > 1:
		issuesToBeProcessed[row[0]] = row

		key = row[0]
		# first, get the very issue itself. It's a query that will return only one issue.
		issues = jira.search_issues('id in (' + key + ')')
		for eachIssue in issues:
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
		if eachIssue.key in processedIssues:
			continue
		issuesToBeProcessed[''+eachIssue.key] = 1
		writer.writerow({'issue id': eachIssue.key, 'why listed': 'child of: ' + key, 'summary': eachIssue.fields.summary})
		sys.stdout.flush()

	issues = jira.search_issues('"Epic Link" in (' + key + ')')
	for eachIssue in issues:
		#print ' > '+ eachIssue
		if eachIssue.key in processedIssues:
			continue
		issuesToBeProcessed[''+eachIssue.key] = 1
		writer.writerow({'issue id': eachIssue.key, 'why listed': 'linked to epic: ' + key, 'summary': eachIssue.fields.summary})
		sys.stdout.flush()

	issues = jira.search_issues('issue in linkedIssues(' + key + ',"requires")')
	for eachIssue in issues:
		#print ' > '+ eachIssue
		if eachIssue.key in processedIssues:
			continue
		issuesToBeProcessed[''+eachIssue.key] = 1
		writer.writerow({'issue id': eachIssue.key, 'why listed': 'required by: ' + key, 'summary': eachIssue.fields.summary})
		sys.stdout.flush()

	issues = jira.search_issues('issue in linkedIssues(' + key + ',"is blocked by")')
	for eachIssue in issues:
		#print ' > '+ eachIssue
		if eachIssue.key in processedIssues:
			continue
		issuesToBeProcessed[''+eachIssue.key] = 1
		writer.writerow({'issue id': eachIssue.key, 'why listed': 'blocks: ' + key, 'summary': eachIssue.fields.summary})
		sys.stdout.flush()


	processedIssues[''+key] = 1
	if ''+key in issuesToBeProcessed:
		del issuesToBeProcessed[''+key]
