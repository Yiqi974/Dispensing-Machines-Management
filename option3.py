# #import csv
# import os
# # ensure your current working directory is where you place all files and folders
# os.chdir("d:\\Documents\\Python files\\YeQuBianCheng\\MSBA\\AN6100\\group project 1")
# print(os.getcwd())

def ProcessDailySales(prompt):
    import csv
    import os
    from datetime import datetime
    while True:
        try:
            thedate = input(prompt).strip()
            # whether date entered is fit for real life
            dateneeded = datetime.strptime(thedate,'%Y-%m-%d').strftime('%Y%m%d')
            # whether date entered is in right format
            date = thedate.split("-")

            # create complete folder if cwd has no such folder
            if not os.path.exists("complete"):
                os.mkdir("complete")

            # situation 1: if files according to date entered in complete folder 
            if any(f"{date[0]}{str(date[1]).zfill(2)}{str(date[2]).zfill(2)}" in file for file in os.listdir("complete")):
                print("All files for the date are completely processed\n")
                
                # ask the user whether he contine to process,NO->break;YES->list pending files/empty folder
                proceedOrNot = input("Do you want to process another date's sales?[Y/N] ").strip().upper()
                if proceedOrNot in ['N','NO']:
                    print("You choose to no longer process other data.")
                    break
                else:
                    # remove additional files automatically created by computer
                    pendingfiles = os.listdir("pending")
                    for i in pendingfiles:
                        if os.path.splitext(i)[1] != ".txt":
                            pendingfiles.remove(i)
                    # if continue, whether the pending folder is empty
                    if pendingfiles != []:
                        print("="*100)
                        print(pendingfiles)
                        print("="*100)
                        print("Choose a date in above list\n")
                    else:
                        print("Empty pending folder, no more files to process")
                        break


            # situation 2: if files according to date entered in pending folder 
            elif any(f"{date[0]}{str(date[1]).zfill(2)}{str(date[2]).zfill(2)}" in fileName for fileName in os.listdir("Pending")):
                # print("file found")
                
                master = []
                with open('master.txt','r') as f:
                    for each in f:
                        s = each.strip().split(",")
                        master.append([s[0],int(s[1]),s[2]])
                #print("master list created")
                # print(master)
                #print("="*30)

                pending = []
                for fileName in os.listdir("Pending"):
                    if fileName.find(f"{date[0]}{str(date[1]).zfill(2)}{str(date[2]).zfill(2)}") >= 0:
                        filePath = "Pending/"+ fileName
                        with open(str(filePath),'r') as f:
                            for each in f.readlines()[1:]:
                                s = each.strip().split(",")
                                pending.append([fileName[1],int(s[1]),int(s[2])])
                #print("pending list created")

                # step 1. add a colume of date based on option 2's data display
                newformatdate = f"{str(date[2]).zfill(2)}/{str(date[1]).zfill(2)}/{date[0]}"
                # print(newformatdate)
                for each in pending:
                    for s in master:
                        if each[0] == s[0] and each[1] == s[1]:
                            each.append(s[2])
                            each.append(newformatdate)
                #print("pending list updated")
                #print(pending)
                #print("="*30)
            
                dic = {}
                for each in pending:
                    #print(each)
                    if str(each[4] + " " + each[0] + " " + each[3]) not in dic.keys():
                        dic[str(each[4] + " " + each[0] + " " + each[3])] = [[str(each[1])],each[2]]
                    else:
                        dic[str(each[4] + " " + each[0] + " " + each[3])][1] += each[2]
                        if str(each[1]) not in dic[str(each[4] + " " + each[0] + " " + each[3])][0]:
                            dic[str(each[4] + " " + each[0] + " " + each[3])][0].append(str(each[1]))
                #print(dic)

                # step 2. replace "," with ";" in slots column
                for key,value in dic.items():
                    dic[key][0] = ";".join(dic[key][0])
                #print(dic)

                print(f"{'date':^10s}{'machineId':<12s}{'productId':^15s}{'Slots':^15s}{'Quantity'}")
                for key,value in dic.items():
                    splitkey = key.split(" ")
                    print(f"{splitkey[0]:<12s} {splitkey[1]:<12s} {splitkey[2]:<14s} {value[0]:<11s} {value[1]}")

                # step 3. write data in summary.csv file
                if "SummarySales.csv" not in os.listdir():
                    with open("SummarySales.csv","a",newline="") as fp:
                        fieldnames = ["date","machineId","productId","slots","Quantity"]
                        summary_writer = csv.DictWriter(fp,fieldnames=fieldnames)
                        summary_writer.writeheader()
                    #print("Header writed")
                        
                    with open("SummarySales.csv","a",newline="") as fp:
                        fieldnames = ["date","machineId","productId","slots","Quantity"]
                        summary_writer = csv.DictWriter(fp,fieldnames=fieldnames)
                        for key,value in dic.items():
                            splitkey = key.split(" ")
                            summary_writer.writerow({'date':splitkey[0],'machineId':splitkey[1],'productId':splitkey[2],'slots':value[0],'Quantity':value[1]})
                    print("Data writed into summarysales file\n")
                else:
                    with open("SummarySales.csv","a",newline="") as fp:
                        fieldnames = ["date","machineId","productId","slots","Quantity"]
                        summary_writer = csv.DictWriter(fp,fieldnames=fieldnames)
                        for key,value in dic.items():
                            splitkey = key.split(" ")
                            summary_writer.writerow({'date':splitkey[0],'machineId':splitkey[1],'productId':splitkey[2],'slots':value[0],'Quantity':value[1]})
                    print("Data writed into summarysales file\n")

                # step 4. after writing to csv, move corresponding files into complete folder
                import shutil
                for fileName in os.listdir("Pending"):
                    if fileName.find(f"{date[0]}{str(date[1]).zfill(2)}{str(date[2]).zfill(2)}") >= 0:
                        filePath = "Pending/"+ fileName
                        if os.path.exists(filePath):
                            targetPath = "complete/"+ fileName
                            # print(targetPath)
                            shutil.move(filePath,targetPath)
                
                # step 5. if pending folder still have files to process, ask user whether to process or not; if no files in pending folder, break
                # remove additional files automatically created by computer
                pendingfolder = os.listdir("pending")
                for i in pendingfolder:
                    if os.path.splitext(i)[1] != ".txt":
                        pendingfolder.remove(i)
                if pendingfolder:
                    print("="*100)
                    print(pendingfolder)
                    print("="*100)
                    print("you still have files waiting to be processed\n")
        
                    proceedOrNot = input("Do you want to continue processing?[Y/N] ").strip().upper()
                    if proceedOrNot in ['Y','YES']:
                        print("Choose a date in above list\n")
                    else:
                        print("You choose to no longer process other data.")
                        break
                else:
                    print("Empty pending folder, you have completed processing all files")
                    break
            

            # situation 3: if valid date input, files for the date don't exist
            else:
                print("File not found, please enter another date!\n")
        
        except:
            print("Error, please enter again!\n")


if __name__ == "__main__":
    ProcessDailySales("Please enter a date to process daily sales[yyyy-mm-dd]: ")
