# DevLogs PWA

This is a simple in-house progressive web app that all software engineers in a team can use to maintain their developer logs/diaries. 

The Senior Software Engineer has given me the following requirements/specifications:  
1. Security evident in all phases of the software development lifecycle  
2. Ability for new team members to self-sign up  
3. Authentication and session management  
4. Developer log entries are time/date stamped  
5. Application meets minimum WC3 PWA standards  
6. Allow developers to search entries by developer, date, project or log/diary contents 
7. The app is modelled using: Level 0 data flow diagram, Structure chart & Data dictionary 
8. Optional: API data sharing and 2FA authentication 

## How to use DevLogs

### Running required files
```bash
python main.py
```
```bash
python api.py
```

### Logging In/Signing Up

> [!TIP]
> Developers can use this working login, Username: TestUser, Password: Test1234%

### Two Factor Authentication

Users need to authenticate themselves using using [Google Authenticator](https://en.wikipedia.org/wiki/Google_Authenticator)
> [!IMPORTANT]
> Users need to remove the space inbetween the code. ![2FA tip](/docs/README_resources/2fa_important.PNG "Follow these steps to test your basic API")

