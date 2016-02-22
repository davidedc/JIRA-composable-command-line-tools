# What

A set of command line tools for working with JIRA. The difference with the other JIRA CLI tools out there is that these tools are meant to work together through pipes and redirections, UNIX-shell-style.

# Quick example

```echo "id = WPS-1532" | python simpleQuery.py |  python allTheWorkNeeded.py | python status.py | python cropSummary.py | csvlook```

<p align="center">
  <img src="https://raw.githubusercontent.com/davidedc/JIRA-composable-command-line-workflows/master/readme-images/img4.png">
</p>

# Setup
You just need python and csvkit. csvkit gives you a number of tools to manipulate .csv files from the command line and can be found at https://csvkit.readthedocs.org/en/0.9.1/ .

# General pattern
Commands can take either a query string or a .csv file as input, and always give a .csv file in output. Since all data is in .csv form, the csvkit tools come extremely handy and can be used for example to do joins, select columns, query the data further... For more information on csvkit please see https://csvkit.readthedocs.org/en/0.9.1/tutorial.html

# Commands

## simpleQuery

Just returns a .csv based on any query you pass, example:

```echo "id = WPS-1532" | python simpleQuery.py```

gives:

```issue id,summary```<br>
```WPS-1532,THE ISSUE SUMMARY HERE```

## cropSummary

takes a .csv and returns the same .csv, but all summaries are cropped so that they fit on screen:

```echo "id = WPS-1532" | python simpleQuery.py | python cropSummary.py ```

gives:

```issue id,summary truncated```<br>
```WPS-1532,THE ISSUE SUM...```

## allTheWorkNeeded

takes a .csv with a list of issues and recursively reaches all the issues that are subtasks, part of an epic, or blocking or required. The output .csv also includes a colunm that explains how each issue is "reached", e.g. is it a child of an issue? is it part of an epic? etc.

Example:

<p align="center">
  <img src="https://raw.githubusercontent.com/davidedc/JIRA-composable-command-line-workflows/master/readme-images/img1.png">
</p>


## status

takes a .csv and returns the same .csv, but with an added column for all the statuses

## lastComment

takes a .csv and returns the same .csv, but with an added column with the last comment for each issue

<p align="center">
  <img src="https://raw.githubusercontent.com/davidedc/JIRA-composable-command-line-workflows/master/readme-images/img2.png">
</p>

## openEpics

takes a query string and finds all open epics that satisfy the query.

<p align="center">
  <img src="https://raw.githubusercontent.com/davidedc/JIRA-composable-command-line-workflows/master/readme-images/img3.png">
</p>
