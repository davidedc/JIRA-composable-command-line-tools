from jira.client import JIRA
import csv
import sys
import time

reader = csv.reader(sys.stdin)
fieldnames = reader.next()

       
newFieldnames = ['summary truncated' if x=='summary' else x for x in fieldnames]


writer = csv.DictWriter(sys.stdout, fieldnames=newFieldnames)
writer.writeheader()

for row in reader:
	rowToBeWritten = {}
	for x in range(0, len(row)):
		
		if fieldnames[x] != 'summary':
			rowToBeWritten[fieldnames[x]] = row[x]
		else:
			rowToBeWritten['summary truncated'] = (row[x][:40] + '..') if len(row[x]) > 40 else row[x]

	writer.writerow(rowToBeWritten)
	sys.stdout.flush()
