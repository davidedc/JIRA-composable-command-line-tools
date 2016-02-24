# What

A set of command line tools for working with JIRA. The difference with the other JIRA CLI tools out there is that these tools are meant to work together (between them and with other .csv-oriented tools already available out there) through pipes and redirections, UNIX-shell-style. So rather than using one huge cli-based tool, one can use this set of simple tools that can be combined to do complex queries and operations, as per examples.

# Quick example

Show all tasks needed to complete an issue, their status and a brief version of their summary:

```echo "id = WPS-1532" | python simpleQuery.py |  python allTheWorkNeeded.py | python status.py | python cropSummary.py | csvlook```

<p align="center">
  <img src="https://raw.githubusercontent.com/davidedc/JIRA-composable-command-line-workflows/master/readme-images/img4.png">
</p>

## "But I don't want to type python"

create an alias:

```alias simpleQuery="python simpleQuery.py"```<br>
```echo "id = WPS-1532" | simpleQuery```

# Setup
You just need python and csvkit (just ```pip install csvkit```). csvkit gives you a number of tools to manipulate .csv files from the command line and can be found at https://csvkit.readthedocs.org/en/0.9.1/ .

Also open the configurationData file, fill-in with your relevant data and delete the ```.example``` part of the extension.

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

takes a .csv and returns the same .csv, but with an added column with the last comment for each issue. This type of listing with the last comment is otherwise impossible to do with JIRA's web interface or any plugin I'm aware of.

<p align="center">
  <img src="https://raw.githubusercontent.com/davidedc/JIRA-composable-command-line-workflows/master/readme-images/img2.png">
</p>

## openEpics

takes a query string and finds all open epics that satisfy the query.

<p align="center">
  <img src="https://raw.githubusercontent.com/davidedc/JIRA-composable-command-line-workflows/master/readme-images/img3.png">
</p>
