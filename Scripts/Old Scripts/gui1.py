import sys
import os
from tkinter import *
import tkinter.font as TkFont
import subprocess as sub

window=Tk()
window.title("Dashboard")
window.geometry('1080x1920')

fontStyle = TkFont.Font(family="Simplifica", size=30)
photo = PhotoImage(file='icon.png')

top_frame = Frame(window, height = 128, width = 1920, pady=3, bg = 'white').grid(row = 1, columnspan = 4)
Label(top_frame, image = photo, bg = 'white').grid(row=1, column=0)
Label(top_frame, text= 'Red Team Automation Solutions', font=fontStyle, foreground="red", bg = 'white').grid(row=1, column = 1)

#side_frame = Frame(window, height = 300, width = 500).grid(rowspan = 8, column = 0)

text_frame = Frame(window, height = 500, width = 500).grid(rowspan = 9, column = 1)

def run(event):
    #myLabel = Label(window, text=getClicked().grid(column = 1, row = 4)
    if variable.get() == "SQL Injection Detector":
        os.system('python3 sql_injection_detector.py http://testphp.vulnweb.com/artists.php?artist=1')
        hi = sub.Popen(['python3','sql_injection_detector.py','http://testphp.vulnweb.com/artists.php?artist=1'], stdout=sub.PIPE,stderr=sub.PIPE) 
        output, errors = hi.communicate()
        text = Text(text_frame)
        text.grid(row = 5, column = 1)
        text.insert(END, output)

    elif variable.get() == "Cross-Site Scripting Detector":
        os.system('python3 xss_scanner.py https://xss-game.appspot.com/level1/frame')
        hi = sub.Popen(['python3','xss_scanner.py','https://xss-game.appspot.com/level1/frame'], stdout=sub.PIPE,stderr=sub.PIPE) 
        output, errors = hi.communicate()
        text = Text(text_frame)
        text.grid(row = 5, column = 1)
        text.insert(END, output)       

    elif variable.get() == "Clickjacking Detector":
        os.system('python3 clickjack.py site.txt')
        hi = sub.Popen(['python3','clickjack.py','site.txt'], stdout=sub.PIPE,stderr=sub.PIPE) 
        output, errors = hi.communicate()
        text = Text(text_frame)
        text.grid(row = 5, column = 1)
        text.insert(END, output)  

    elif variable.get() == "Subdomain Detector":
        os.system('python3 subdomain.py')
        hi = sub.Popen(['python3','subdomain.py'], stdout=sub.PIPE,stderr=sub.PIPE) 
        output, errors = hi.communicate()
        text = Text(text_frame)
        text.grid(row = 5, column = 1)
        text.insert(END, output) 

    elif variable.get() == "Multi-Threaded Subdomain Detector":
        os.system('python3 threaded_subdomain.py google.com -l subdomains.txt -t 10')
        hi = sub.Popen(['python3','threaded_subdomain.py','google.com -l subdomains.txt -t 10'], stdout=sub.PIPE,stderr=sub.PIPE) 
        output, errors = hi.communicate()
        text = Text(text_frame)
        text.grid(row = 5, column = 1)
        text.insert(END, output) 

    elif variable.get() == "External/Internal Links Detector":
        os.system('python3 link_extractor.py https://github.com -m 2')
        hi = sub.Popen(['python3','link_extractor.py','https://github.com -m 2'], stdout=sub.PIPE,stderr=sub.PIPE) 
        output, errors = hi.communicate()
        text = Text(text_frame)
        text.grid(row = 5, column = 1)
        text.insert(END, output)

    else:
        print(variable.get())
        pass

options = [
"SQL Injection Detector",
"Cross-Site Scripting Detector",
"Clickjacking Detector",
"Subdomain Detector",
"Multi-Threaded Subdomain Detector",
"External/Internal Links Detector"
] 

variable = StringVar()
variable.set(options[0])

drop = OptionMenu(window, variable, *options, command=run)
drop.grid(column = 0, row = 4)

Clicked = variable.get()

#Label(side_frame , text=" ").grid(row=2, column = 1)
window.mainloop()