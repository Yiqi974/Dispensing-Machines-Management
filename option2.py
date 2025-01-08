def Pre_sales_view():
    
    file = []
    
    while True:
        try:
            from datetime import datetime
            #urge the user use the standard format
            thedate = input('Please enter the date to preview [YYYY-MM-DD]: ') 
            #convert the formal date yyyy-mm-dd to yyyymmdd 
            date_need = datetime.strptime(thedate,'%Y-%m-%d').strftime('%Y%m%d') 
    
            #double check option1:right format but not in pending file yet option2: wrong format like 1223-13-03,20220728  
            import os
            flag = 0
            for each in os.listdir('pending'): 
                if date_need in each:
                    file.append(each)
                    flag += 1
    
            if flag == 0:
                print("File not found, please enter another date!\n") 
            else:
                break
        except:
            print("Error input, please enter again")
        
    
    #iterate machineID,slotID,productID in masterfile
    masterfile = []
    with open('master.txt') as f:
        for each in f:
            s = each.strip().split(",")
            masterfile.append([s[0],int(s[1]),s[2]])

    #switch positions of slotID and productID
    for i in range(len(masterfile)):
        masterfile[i][1],masterfile[i][2] = masterfile[i][2],masterfile[i][1]
    
    #iterate machineID,slotID,quantity in pendingfile through input date               
    pendingfile = []
    for each in file:
        if date_need in each:
            with open('.\\pending\\'+each,'r') as f:
                for each1 in f.readlines()[1:]:
                    s = each1.strip().split(",")
                    del s[0]
                    pendingfile.append([each.split('_')[0][1:],int(s[0]),int(s[1])]) 
    
    #combine masterfile and pendingfile   
    mas_penfile=[]
    for i in pendingfile:
        for j in masterfile:
            if i[0] == j[0] and i[1] == j[2]:
                i.append(j[1])
                mas_penfile.append(i)       
    
    #add up quantity and slot-ID of each product
    dic = {}
    for i in mas_penfile:
        if str(i[0]+" "+i[3]) not in dic.keys():
            dic[str(i[0]+" "+i[3])] = [i[2],[i[1]]]
        else:
            dic[str(i[0]+" "+i[3])][0] += i[2]
            if i[1] not in dic[str(i[0]+" "+i[3])][1]:
                dic[str(i[0]+" "+i[3])][1].append(i[1]) 
    
    #print out the result
    print(f"{'MachineID':<14s}{'ProductID':<14s}{'Quantity':<15}{'Slot-ID'}")
    for key, value in dic.items():
        value[1] = ','.join([str(i) for i in value[1]])
        print(f"{key.split(' ')[0]:<14s}{key[2:]:<14s}{value[0]:<15}{value[1]}")           
            

    



        




