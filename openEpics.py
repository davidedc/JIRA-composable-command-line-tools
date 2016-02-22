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

fieldnames = ['issue id', 'summary']
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

rowNumber = 0
queryFromStdin = sys.stdin.readline()

issues = jira.search_issues("project = SRM and status != resolved and status != Closed and " + queryFromStdin)

for eachIssue in issues:
	summary_truncated = (eachIssue.fields.summary[:40] + '..') if len(eachIssue.fields.summary) > 40 else eachIssue.fields.summary
	writer.writerow({'issue id': eachIssue.key, 'summary': eachIssue.fields.summary})
	sys.stdout.flush()
