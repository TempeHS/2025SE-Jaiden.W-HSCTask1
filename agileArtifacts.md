# Agile Artifacts
## Sprint backlog list of achievables (annotate changes made during sprint, including data required) 
- ~~Log all failed login attempts and implement a failed login policy, including a strong rate limiting for login page~~
- ~~API data sharing~~ 
- ~~2FA authentication~~
- Create and implement CSS for all pages, including ~~sign-up, login, log/diary entry~~, entries
- SQLite database design and integration for ~~login/sign-up, log/diary entry~~, entries
- ~~Input sanitisation for login/sign-up and log entries~~

## Increment (what must be achieved by the end of the sprint)
- Implement a failed login policy which includes a strong rate limit
- Implement an API for data sharing between the front-end and back-end
- Designed and created the log/diary entry page that is integrated with the database
- Input sanitisation for logs

## Sprint Review (Focus on project management)
### What challenges did you have
 - Had an issue with my implementation of a rate limiter. It was applying to both GET and POST request which was undesirable. Eventually this was fixed. 
 - When initially adding 2FA, the authentication token wasn't unique for each user. This was fixed after generating unique OTP secrets for each user and storing it within the database. 
### What did you do well
- I successfully added an API to my PWA. This effectively handles data between the front-end and back-end for my app. 
- I sanitised inputs for both log entries and login/sign-in to prevent any malicious code being put in.  
### What will you do differently next time
- I'll implement more logging to help with debugging. The logs were helpful for troubleshooting problems and also making the app more secure. 
- Abstract more of my code to separate files so I can reuse code in future projects e.g sanitize.py
