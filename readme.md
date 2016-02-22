# What

A set of command line tools for working with JIRA. The difference with the other JIRA CLI tools is that these tools are meant to work together through pipes and redirections, UNIX-shell-style.

# Quick example

```echo "id = WPS-1532" | python simpleQuery.py |  python allTheWorkNeeded.py | python status.py | python cropSummary.py | csvlook```

<p align="center">
  <img src="https://raw.githubusercontent.com/davidedc/JIRA-composable-command-line-workflows/master/readme-images/img4.png">
</p>

# Setup
You just need python and csvkit. csvkit gives you a number of tools to manipulate .csv files from the command line and can be found at https://csvkit.readthedocs.org/en/0.9.1/ .

# General pattern
Commands can take either a query string or a .csv file as input, and always give a .csv file in output.

# Commands

## simpleQuery

Just returns a .csv based on any query you pass, example:

```echo "id = WPS-1532" | python simpleQuery.py```

gives:

```issue id,summary```
```WPS-1532,THE ISSUE SUMMARY HERE```

## cropSummary

takes a .csv and returns the same .csv, but all summaries are cropped so that they fit on screen:

```echo "id = WPS-1532" | python simpleQuery.py | python cropSummary.py ```

gives:

```issue id,summary truncated```
```WPS-1532,THE ISSUE SUM...```

## allTheWorkNeeded

takes a .csv with a list of issues and recursively reaches all the issues that are subtasks, part of an epic, or blocking or required.

Example:

<p align="center">
  <img src="https://raw.githubusercontent.com/davidedc/JIRA-composable-command-line-workflows/master/readme-images/img1.png">
</p>


## status

takes a .csv and returns the same .csv, but with an added column for all the statuses

## lastComment

takes a .csv and returns the same .csv, but with an added column with the last comment for each issue

## openEpics

takes a query string and finds all open epics that satisfy the query.
