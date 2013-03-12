---
layout: home
title: NYC Canvasing data
---

# Trial Run - Sandy canvas

A large group of Beacon High School students are canvasing neighborhoods effected by Hurricane Sandy. This data will be made available to the Data Anywhere Project to test our system.

Because the canvas will cover many areas of NYC the canvas questions have been split into **common core questions** and **localized questions**

## What needs to get done?

The question as a whole need to be mapped to a document oriented data structure. This means developing a legend to map the human readable questions to their machine readable alternatives. The following naming convention was put together at the last hackathon:

NOTES and CONVENTIONS for COLUMN HEADERS for use in LEGEND
1. All lowercase, even abbreviations (e.g. FEMA)
2. No spaces, use dashes
3. Column name convention is VERB + (NOUN + ADJ?)+ with most general noun first then less specific nouns
4. Naming convention allows, e.g, decorator that retrieves all need fields, and then can refine from general to specific
5. Exception to #3: initial 'note' is a prose note field. Note is first so as not to clutter retrieval as in rule #4.
6. Exception to #3: initial 'project' is a column header that can only be fully understood by consulting subject matter expert from projects
7. Implied subject of all #3 sentences is the contact, e.g. have-electricity means The contact being interviewed has electricity.
8. All have and need columns have Boolean values. All past tense verbs (registered) have Boolean values.

This legend will be part of the function to import a `.csv` file into the database.

## Desired Outcomes

1. A parse and load script much like: [`/occupysandy/db_injection/parse-and-load.py`](https://github.com/dhornbein/DataAnywhere/blob/master/occupysandy/db_injection/parse-and-load.py)
2. A work flow for getting data into the system using the parse-and-load like script.

Ideally this workflow and script will be generic enough to re-use.

# The Canvas Forms:

## Common questions

The following document represents the current "common" question form.

<iframe src="https://docs.google.com/document/d/1sQkfvuqAwGr3-DSN0kmMNXPMSIZnx-8ZDKIlFGL869A/pub?embedded=true" style="width:100%; height:500px;">&nbsp;</iframe>

[View online](https://docs.google.com/document/d/1sQkfvuqAwGr3-DSN0kmMNXPMSIZnx-8ZDKIlFGL869A/pub)

## Location Specific Questions

Because each location has it's own needs they have developed their own questions. Below are the YANA (East Rockaway) questions and Cornaga (also Rockaway) location specific questions. These will be in addition to the common questions above.

### YANA

<iframe src="https://docs.google.com/document/d/1Nhuthrbm6oDExrB2Dde4EoWqIRPuHgLAEEQ2dpMi3AM/pub?embedded=true" style="width:100%; height:300px;">&nbsp;</iframe>

[View online](https://docs.google.com/document/d/1Nhuthrbm6oDExrB2Dde4EoWqIRPuHgLAEEQ2dpMi3AM/pub)

### Cornage

<iframe src="https://docs.google.com/document/d/1ywTedUOtUgWr7jsUIRJKAgzsCKc-5WdAXiqC0o4KYfg/pub?embedded=true" style="width:100%; height:300px;">&nbsp;</iframe>

[View online](https://docs.google.com/document/d/1ywTedUOtUgWr7jsUIRJKAgzsCKc-5WdAXiqC0o4KYfg/pub)