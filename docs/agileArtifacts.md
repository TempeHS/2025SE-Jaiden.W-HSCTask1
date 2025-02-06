# Agile Artifacts
## Sprint backlog list of achievables (annotate changes made during sprint, including data required) 
- Application meets minimum WC3 PWA standards   
- Implement server logs to monitor for unusual activity
- Minimise vulnerabilities in user action controls including broken authentication and session management, cross-site scripting (XSS) and cross-site request forgery (CSRF), invalid forwarding and redirecting, and race conditions  

## Increment (what must be achieved by the end of the sprint)
- Application meet minimum WC3 PWA standards
- Server logs are implemented 
- Vulnerabilites in user action controls are minimised 

## Sprint Review (Focus on project management)
### What challenges did you have
- Implementing session locks was tricky. I'm not 100% sure it works as intended but should help minimise race conditons. 
- Had troubles navigating some issues arising from the browser developer tools. I wasn't sure if the issue arised from my app or external factors 
### What did you do well
- Implement specific countermeasures for each vulnerability listed above.
- Added server logs to monitor for unusual activity and debugging.
### What will you do differently next time
- Constantly code review to check for any security risks and vulnerabilities 
- Be more aware of invalid forwarding and redirecting, making sure to use 'url_for' for flask applications

