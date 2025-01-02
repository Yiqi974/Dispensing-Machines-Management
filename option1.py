# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 12:33:31 2022

@author: Brynn
"""
import os

def MachineEdit():   

    ### use while loop for choice until input is valid
    while True:
       choice = input('''
\tEnter 1: Display machine information
\tEnter 2: Edit machine information\n
Please enter your choice: ''').strip()
       if choice == '1' or choice == '2':
           break
       else:
           print('Invalid input, please enter again!')
           
    ### choice1: display information       
    if choice == '1':       
    ### use while loop for input until input is valid
        while True:
            try:
                machineID = input('Please enter the machine ID(only 1 integer): ').strip()
                machineIDTest = int(machineID)
                break
            except:
                print('Invalid input,please enter again!')
        
        slotList = ['Slot-ID']
        productIDList = ['Product-ID']
        with open('master.txt','r') as fm:
            for line in fm.readlines():        # check each line for info of the selected machine
                line = line.split(',')
                if line[0] == machineID:
                    slotList.append(line[1])
                    productIDList.append(line[2])
            if len(slotList) > 1 and len(productIDList) > 1:    # every list at least has 1 element except the title if not a new machine
                for i in range(len(slotList)):
                    print(f"{slotList[i]:^7s} {productIDList[i]:^11s}\n")
            else:
                print('This is a new machine!')
        return False
    
    ###choice2:Edit information
    if choice == '2':
    ### check if there are still files to be processed in pending folder 
        pendingFlag = False
        path = 'pending'
        files = os.listdir(path)
        if files:
            print('There are still files in pending, please process them first!')
            pendingFlag = True
            return pendingFlag     # exist files to be processed, end this function and return a flag to main.py
        
        ### use while loop for machine-ID input until input is valid
        while True:
            machineID = input('''Please enter the machine ID you wanna edit:
           1.Spaced by commas:1,2,…
           2.If edit all machines, please enter "all"\n''').lower().split(',')
            correctFlag = True
            for each in machineID:
                if each == 'all' and len(machineID) == 1:
                    break
                try:
                    machineIDTest = int(each)
                except:
                    correctFlag = False
                    print('Invalid machine ID, please enter again!')
                    break
            if correctFlag:
                break
                
        machineIDOrigin = []  # a list for saving all the machine-IDs in original master.txt
        with open('master.txt','r') as fm:  # save all the machine-IDs in original master.txt to list
            for line in fm.readlines():
                line = line.split(',')
                if line[0] not in machineIDOrigin:
                    machineIDOrigin.append(line[0])
        
        if machineID == ['all']:
            machineID = machineIDOrigin
            
        with open('master.txt','r') as f_r:  # read all the info in original master.txt
            lines = f_r.readlines()
            
         ### use while loop for choosing operation until input is valid
        while True:
            operation = input('''How do you want to edit the information?
            Enter 1: Add or Amend information with Slot-ID
            Enter 2: Remove whole slot information
            Enter 3: Remove entire machine profile\n''').strip()
            if operation == '1' or operation == '2' or operation == '3':
                break
            else:
                print('Invalid input, please enter again!')
         ### operation1:add or amend the slot-ID and the product-ID of the chosen machine
        if operation == '1':
            ### use while loop to check the format of slot-ID and product-ID input until it is valid
            while True:
                slotFlag = True
                slotAmend = input('Please enter the Slot-ID and the Product-ID(1 letter and 3 numbers)(Spaced with commas):\n').upper()
                if ',' not in slotAmend:
                    slotFlag = False
                else:
                    slotAmend = slotAmend.split(',')
                    if len(slotAmend) == 2 and len(slotAmend[1]) == 4 and slotAmend[1][0].isalpha():
                        try:
                            slotAmendTest = int(slotAmend[0])
                            slotAmendproTest = int(slotAmend[1][1:4])
                        except:
                            slotFlag = False
                    else:
                        slotFlag = False
                if slotFlag:
                    break
                else:
                    print('Invalid input, please enter again!')
            
            with open('master.txt','w') as f_w:
                for line in lines:                         # find the matching slot-ID in each line
                    line = line.split(',')
                    if line[0] in machineID and line[1] == slotAmend[0]:  # if machine-ID exists and slot-ID exists,amend the original ones
                        line = line[0]+','+slotAmend[0]+','+slotAmend[1]+'\n'
                        machineID.remove(line[0])          # remove the machine-ID whose slot has been amended   
                    if isinstance(line,list):              # write the current line into master.txt
                        f_w.write(",".join(line))          # if not amended,line is a list
                    else:
                        f_w.write(line)                    # if amended,line is a str
                   
                if machineID:  # when loop ends and there still exists ID in machineID[],
                    for ID in machineID:  # at least one of machineID and slot-ID is new, add new lines
                        line =ID +','+slotAmend[0]+','+slotAmend[1]+'\n'
                        f_w.write(line)
                     
         ### operation2:remove the slot-ID and the product-ID of the chosen machine                 
        if operation == '2':
            ### use while loop to check the input of slot-ID until it is an integer
            while True:
                try:
                    slotRemove = input('Please enter the Slot-ID you wanna remove(only 1 integer):\n').strip()
                    slotRemoveTest = int(slotRemove)
                    break
                except:
                    print('Invalid input,please enter again!')
            
            with open('master.txt','w') as f_w:
                for line in lines:                # find the matching machine-ID and slot-ID in each line
                    line = line.split(',')
                    if line[0] in machineID and line[1] == slotRemove: # if both the machine-ID and slot-ID match,remove the record
                        machineID.remove(line[0]) # remove the machine-ID whose slot has been amended 
                        continue
                    f_w.write(",".join(line)) 
                   
                if machineID:  # when loop ends and there still exists ID in machineID[],
                    print('New slot-ID or new machine-ID,cannot be removed!')  # at least one of machineID and slot-ID is new, no record can be removed
        
         ### operation3:remove the entire profile of the chosen machine               
        if operation == '3':
            with open('master.txt','w') as f_w:
                for ID in machineID:    
                    if ID not in machineIDOrigin:  # check if machine-ID exists
                        machineID.remove(ID)       # if not, then new machine, remove from the desiring machine-ID list
                        print('MachineID'+ ID +'does not exist,cannot be removed!') # new machine profile cannot be removed
                if machineID:       # the left IDS are machine-IDs which exist
                    for line in lines:       # find matching machine-ID in each line
                        line = line.split(',')
                        if line[0] in machineID:
                            continue               # if is the chosen machine-ID,skip the write operation(remove)
                        else:
                            f_w.write(",".join(line))  # not the chosen machine-ID, write the original records
        
        return pendingFlag      

if __name__ == '__main__':
    if MachineEdit():
        print('warning')
    