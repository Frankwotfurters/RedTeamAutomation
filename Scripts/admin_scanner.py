import urllib.request
import os
import time
import sys
from colorama import init, Fore
import rpa as r
import requests
from fpdf import FPDF



# def getTarget():
#     target = request.form['target']
#     return target

def main(target):
    #target = request.form.get['target']
    #Define colours for different outputs
    
    #Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=16)
    pdf.cell(200, 10, txt="RTA Integrated RPA", ln=2, align='L')
    pdf.set_font('')
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt="Scanner: Admin Interface", ln=1, align='L')
    timestart = time.strftime("%d/%m/%Y %I:%M:%S")
    time1 = time.strftime("%-H%M")
    pdf.cell(200, 10, txt=f"Scan Time: {timestart}", ln=1, align="L")
    pdf.cell(200, 10, txt="Results: ", ln=1, align='L')

    GREEN = Fore.GREEN
    RED = Fore.RED
    BLUE = Fore.BLUE

    print(" ")
    print(f"{BLUE}ADMIN INTERFACE SCANNER")
    print(" ")

    #User can input what website they want to run the scanner on
    try:
        # if target.endswith("/"):
        #     print("Target: ",target)
        # else:
        #     print('Please follow the recommended format!')
        #     exit()
        # target = input(f"{BLUE}ENTER WEBSITE: ")
        # targetlist = open("target.txt", "r")
        # target = targetlist.read()
        # targetlist.close() 
        print("Target: ",target)
        pdf.cell(200, 10, txt="Target Scanned: "+target, ln=1, align="L")
            

    #If user interrupts scanner (CTRL C). The scanner will stop and print a message.
    except KeyboardInterrupt:
        print(f"{RED}\nUSER INTERRUPTED. CLOSING SCANNER.")
        exit()

    print(" ")
    print(time1,f"{GREEN}[+] STARTING SCAN ON " + target)
    #pdf.cell(200, 10, txt=f"Scan Start Time: {time1}", ln=1, align="L")

    #Create an empty array to store admin pages that were found
    admin = []

    #Retrieve wordlist from another file
    #r means read 
    wordlist = open("admin_wordlist.txt", "r")
    #wordlist_readlines() will allow the loop to read line by line
    list1 = wordlist.readlines()
    #list2 = list1.rstrip()
    ss = []
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
            imgtime = time.strftime("(%d%m-%I%M%S)")
            time2 = time.strftime("[%I:%M:%S]")
            print(time2,f"{GREEN}[+] FOUND POSSIBLE ADMIN PAGE:",curl)
            #pdf.cell(200, 10, txt="[+] FOUND POSSIBLE ADMIN PAGE:"+ curl, ln=1, align="L")
            r.init()
            r.url(curl)
            r.wait()
            ss.append(f"admin-scanner-{imgtime}.png")
            r.snap("page", f"admin-scanner-{imgtime}.png")
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
        #pdf.cell(200, 10, txt=f"Scan End Time: {time3}", ln=1, align="L")
        pdf.cell(200, 10, txt="Summary:", ln=1, align="L")
        pdf.cell(200, 10, txt="[-] Website is vulnerable.", ln=1, align="L")
        pdf.cell(200, 10, txt="[-] Vulnerability Detected: OWASP Top 10 - Security Misconfigurations", ln=1, align="L")
        pdf.cell(200, 10, txt="[-] Scanner was able to locate admin page(s) of website", ln=1, align="L")
        pdf.cell(200, 10, txt="[-] Possible admin page(s): ", ln=1, align="L")
        
        #New array to omit the "\n" from the admin array
        admin2 = [ ]
        for i in admin:
            admin2.append(i.strip())

        print(admin2)
        pdf.cell(200, 10, txt=f"{admin2}\n", ln=1, align="L")

    else:
        print(f"{GREEN}[+] WEBSITE IS NOT VULNERABLE.")
        print(f"{GREEN}[+] SCANNER WAS UNABLE TO LOCATE ADMIN PAGE(S).")
        pdf.cell(200, 10, txt="[+] Website is not vulnerable", ln=1, align="L")
        pdf.cell(200, 10, txt="[+] Scanner was unable to locate admin page(s)", ln=1, align="L")

    print(" ")
    pdf.cell(40, 10, txt=f"Screenshot(s) of POC will be in the following page(s).", ln=1, align="L")
    print(f"{BLUE}END OF RESULT")

    pdf.cell(200, 10, txt="End of Results.", ln=1, align="L")
    # To add screenshots of all vulnerable pages to the PDF Report
    for i in ss:
        pdf.add_page(orientation="L", format="A4")
        pdf.set_font('Arial', size=12)
        pdf.cell(200, 10, txt=f"Proof of Concept ({i})", ln=1, align='L')
        pdf.image(f'/media/sf_Shared_VM_Folder/RedTeamAutomation/Scripts/{i}',50,50,300,120)
    
    pdf.output(f'adminscan({time1}).pdf')

    #RPA (To open PDF file after scan)
    displayfile = []
    displayfile.append(f"adminscan({time1}).pdf")

    outputfile = (f"adminscan({time1}).pdf")
    r.init(visual_automation=True)
    r.clipboard(f"file:///media/sf_Shared_VM_Folder/RedTeamAutomation/Scripts/{outputfile}")
    r.url()
    r.keyboard("[ctrl]l")
    r.keyboard("[ctrl]v")
    r.keyboard("[enter]")

    #Display PDF link on results page
    results = {}
    results["displayfile"] = displayfile
    return results

if __name__ == "__main__":
    main()