# RPA Integrated RTA
Current red teaming processes include many manual tasks that are often repetitive, undermining the efficiency and productivity of red team auditors. Red Team Automation with Robotic Process Automation Integration (RPA Integrated RTA) is a project that aims to enhance red teaming by eliminating repetitive manual processes with the use of RPA. Software robots can understand what is on the screen, type the correct keystrokes, recognise/retrieve data, and do various pre-defined tasks. With RPA, repetitive manual tasks can be automated, allowing red team auditors to focus on more complex issues.

![alt text](https://github.com/Frankwotfurters/RedTeamAutomation/blob/main/Scripts/homepage.png)

# Main Features
- Scanners developed based on the [**OWASP Top 10**](https://owasp.org/www-project-top-ten/) vulnerabilities 
- RPA Integration
- Automatic PDF Generation
- Email Notification
- Logging
- User Friendly GUI

# Scanners
Scanner|Function
:-------|:---------
Sensitive Data Exposure Scanner|Scans for the error message that displays after an unsuccessful login
Link Extractor|Uses RPA + Python Scripting tool that crawls every page of a website to extract data
Admin Interface Scanner|Uses RPA + Python Scripting to scan for vulnerable/exposed admin interfaces using a curated wordlist of commonly used admin page names.
Clickjacking Scanner|Uses RPA + Python Scripting to check if website is vulnerable to clickjacking and creates a PoC
Cross Site Scripting Scanner|Uses RPA + Python Scripting to demonstrate and detect XSS vulnerabilities
Cross-Site Request Forgery Scanner|Scans for possibly vulnerable forms using RPA and creates a testing PoC CSRF webpage
Using Components with Known Vulnerabilities Scanner|Scans all JS files loaded by a website and server version for known vulnerabilities with help from RPA
SQL Injection Detector|Uses RPA + Python Scripting to demonstrate and detect SQL injection vulnerabilities
Subdomain Scanner|Uses RPA + Python Scripting to locate and explore the full domain infrastructure of a website

# Technology Used
- [**Visual Studio Code**](https://code.visualstudio.com/)
- [**RPA with Python**](https://github.com/tebelorg/RPA-Python)
- [**Flask**](https://flask.palletsprojects.com/en/2.0.x/)
- [**Python**](https://www.python.org/downloads/)
- [**Kali Linux**](https://www.kali.org/)

# Setup
Clone the repo
```
git clone https://github.com/Frankwotfurters/RedTeamAutomation
```
Run the automatic setup script
```
cd RedTeamAutomation/Scripts && chmod a+x setup.sh && ./setup.sh
```
Do it all in one line
```
git clone https://github.com/Frankwotfurters/RedTeamAutomation && cd RedTeamAutomation/Scripts && chmod a+x setup.sh && ./setup.sh
```
