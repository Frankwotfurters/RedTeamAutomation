import os.path
import os
import time

def scan_report():
    #Define current path
    pwd = os.path.dirname(os.path.realpath(__file__))
    
    #List all files
    files = os.listdir(pwd)

    username = []
    scanner = []
    pdf_path = []
    time1 = []
    time2 = []

    #Scanner Name
    for name in files:
        if name.endswith(".pdf"):
            name_1 = name.split("_",2)
            name_2 = name_1[1]
            scanner.append(name_2)

    #Date
    for date in files:
        if date.endswith(".pdf"):
            date_1 = date.strip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.')
            date_2 = date_1[0:10]
            time1.append(date_2)

    #Time
    for time in files:
        if time.endswith(".pdf"):
            time_1 = time.strip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.')
            time_2 = time_1[10:18]
            time2.append(time_2)

    #File Path
    for path in files:
        if path.endswith(".pdf"):
            filepath = os.path.join(pwd,path)
            pdf_path.append(filepath)

    #Username
    for user in files:
        if user.endswith(".pdf"):
            user_1 = user.split("_",1)
            user_2 = user_1[0]
            username.append(user_2)


    results = {}
    results["scanner"] = scanner
    results["time1"] = time1
    results["time2"] = time2
    results["pdf_path"] = pdf_path
    results["username"] = username
    return results

if __name__ == "__main__":
    scan_report()