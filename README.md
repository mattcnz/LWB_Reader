# LWB_Reader
Downloads the Lakes Weekly Bulletin 

Running **download_past_issues.py** will create the folder "LWB Issues" in the directory you run the script from, and download every past issue of the Lakes Weekly Bulletin. If you'd only like to download a few issues, you can edit "for entry in issueArray:" to "for entry in issueArray[0:5]:" to download the first 5, for example.

**download_past_issues** sets up an SQLite database, lwbdb, which contains one table ISSUES (issueID INTEGER PRIMARY KEY ASC, path TEXT NOT NULL, size INTEGER, date TEXT).

Running  **download_latest_issue.py** downloads the latest issue, saves the pdf to the LWB Issues folder, and adds the issue number/date/etc to the database. 
Currently it uses the time the script is run as the date to add to the database, so it would be sensible to run it once a week on the day the issue comes out - perhaps via a scheduler. 


