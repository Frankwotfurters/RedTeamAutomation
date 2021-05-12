import urllib.request
import os
import time
import sys
from colorama import init, Fore
import rpa as r

#Define colours for different outputs
GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE

print(" ")
print(f"{BLUE}ADMIN INTERFACE SCANNER")
print(" ")

#User can input what website they want to run the scanner on
try:
    # target = input(f"{BLUE}ENTER WEBSITE: ")
    targetlist = open("target.txt", "r")
    target = targetlist.read()
    targetlist.close() 
    print("Target: ",target)
        

#If user interrupts scanner (CTRL C). The scanner will stop and print a message.
except KeyboardInterrupt:
    print(f"{RED}\nUSER INTERRUPTED. CLOSING SCANNER.")
    exit()

print(" ")
time1 = time.strftime("[%I:%M:%S]")
print(time1,f"{GREEN}[+] STARTING SCAN ON " + target)

#Create an empty array to store admin pages that were found
admin = []

#Retrieve wordlist from another file
#r means read 
wordlist = open("admin_wordlist.txt", "r")
#wordlist_readlines() will allow the loop to read line by line
list1 = wordlist.readlines()
#list2 = list1.rstrip()

for i in list1:
    #Combine the website URL and the admin page name
    curl = target + i
    try:
        #Try to open the URL and see if there is a connection
        #If there is no connection, it would raise an error. 
        openurl = urllib.request.urlopen(curl)

    except urllib.error.URLError:
        #If there is an error, nothing will happen.
        pass

    except KeyboardInterrupt:
        #If user interrupts (CTRL C)
        print(f"{RED}\nUSER INTERRUPTED. CLOSING SCANNER.")
        exit()

    except ValueError:
        exit(f"{RED}\nERROR OCCURED! PLEASE TRY AGAIN.")

    else:
        #If there is no error and the admin page was found, it will append to the array.
        if curl in admin:
            break
        admin.append(curl)
        time2 = time.strftime("[%I:%M:%S]")
        print(time2,f"{GREEN}[+] FOUND POSSIBLE ADMIN PAGE:",curl)
        r.init()
        r.url(curl)
        r.wait()
        r.snap("page", f"admin-scanner-{time2}.png")
        r.close()
        
        
#print(f"{GREEN}[+] NO. OF ADMIN PAGE NAMES CHECKED AGAINST: " + totalcheck)
time3 = time.strftime("[%I:%M:%S]")
print(time3, f"{GREEN}[+] SCAN COMPLETE")
print(" ")
print(f"{BLUE}RESULTS:")
print(" ")

#If the array is not empty, website is vulnerable.
if admin:
    print(f"{RED}[-] WEBSITE IS VULNERABLE.")
    print(f"{RED}[-] VULNERABILITY DETECTED: OWASP 2017 A6 [SECURITY MISCONFIGURATIONS]")
    print(f"{RED}[-] SCANNER WAS ABLE TO LOCATE ADMIN PAGE(S) OF WEBSITE")
    print(f"{RED}[-] POSSIBLE ADMIN PAGE(S): ")
    
    #New array to omit the "\n" from the admin array
    admin2 = [ ]
    for i in admin:
        admin2.append(i.strip())

    print(admin2)

else:
    print(f"{GREEN}[+] WEBSITE IS NOT VULNERABLE.")
    print(f"{GREEN}[+] SCANNER WAS UNABLE TO LOCATE ADMIN PAGE(S).")

print(" ")
print(f"{BLUE}END OF RESULT")