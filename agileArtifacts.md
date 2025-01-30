# Agile Artifacts
## Sprint backlog list of achievables (annotate changes made during sprint, including data required) 
- ~~Create and implement CSS for all pages, including ~~sign-up, login, log/diary entry~~, entries~~
- ~~SQLite database design and integration for ~~login/sign-up, log/diary entry~~, entries~~
- ~~Developer log entries are time/date stamped~~
- ~~Allow developers to search entries by developer, date, project or log/diary contents~~
- ~~Users given the option to download or delete their data~~
- ~~Authentication and session management~~

## Increment (what must be achieved by the end of the sprint)
- Create page for log entries that can be filtered to search for specific entries
- Users are given to option to delete or download their data 
- Implement session managment to further secure the app 

## Sprint Review (Focus on project management)
### What challenges did you have
- The manifest is getting blocked by the content security policy. I will resolves this in a future sprint.
- I had struggles with implementing session management. Had to change my index.html to an authenticated page for it to work.
### What did you do well
- I abstracted lines of code from main.py to separate files to promote reusability and better readability.
- I effectively integrated the database for the entry page. Accessing the database to GET log entries and display it  to  the user.
### What will you do differently next time
- I will abstract more of my code earlier, making sure it isn't an afterthought.
- Use the browser developer tools more. It will help me with debugging and looking for any issues. 
