import os.path
import os

def report_filter(target, Filterdate):
    #Define current path
    pwd = os.path.dirname(os.path.realpath(__file__))
    
    #List all files
    files = os.listdir(pwd)

    scanner = []
    pdf_path = []
    time1 = []
    time2 = []

    
    #Scanner Name
    for name in files:
        if name.endswith(".pdf"):
            if Filterdate in name and name.startswith(target):
                name_1 = name.split("_",1)
                name_2 = name_1[0]
                scanner.append(name_2)
                

    #Date
    for date in files:
        if date.endswith(".pdf"):
            if Filterdate in date and date.startswith(target):
                date_1 = date.strip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.')
                date_2 = date_1[0:10]
                time1.append(date_2)

    #Time
    for time in files:
        if time.endswith(".pdf"):
            if Filterdate in time and time.startswith(target):
                time_1 = time.strip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.')
                time_2 = time_1[10:18]
                time_3 = time_2[:2] + ":" + time_2[2:]
                time_4 = time_3[:5] + ":" + time_3[5:]
                time2.append(time_4)

    #File Path
    for path in files:
        if path.endswith(".pdf"):
            if Filterdate in path and path.startswith(target):
                filepath = os.path.join(pwd,path)
                pdf_path.append(filepath)

    results = {}
    results["scanner"] = scanner
    results["time1"] = time1
    results["time2"] = time2
    results["pdf_path"] = pdf_path
    return results

if __name__ == "__main__":
    report_filter()