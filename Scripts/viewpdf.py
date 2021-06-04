import os.path
import os
import time

def scan_report():
    #Define current path
    pwd = os.path.dirname(os.path.realpath(__file__))
    
    #List all files
    files = os.listdir(pwd)

    user = []
    pdf_time = []
    pdf_path = []
    time1 = []
    time2 = []

    for name in files:
        if name.endswith(".pdf"):
            name_1 = name[:-4]
            name_2 = name_1.strip('0123456789_.-')
            user.append(name_2)
            print(name_2)

    for date in files:
        if date.endswith(".pdf"):
            date_1 = date.strip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.')
            date_2 = date_1[0:10]
            time1.append(date_2)
            print(date_2)

    for time in files:
        if time.endswith(".pdf"):
            time_1 = time.strip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.')
            time_2 = time_1[10:18]
            time2.append(time_2)
            print(time_2)

    
    for path in files:
        if path.endswith(".pdf"):
            filepath = os.path.join(pwd,path)
            pdf_path.append(filepath)
            print(os.path.join(pwd,path))

    results = {}
    results["user"] = user
    results["time1"] = time1
    results["time2"] = time2
    results["pdf_path"] = pdf_path
    return results

if __name__ == "__main__":
    scan_report()