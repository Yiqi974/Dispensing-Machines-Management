#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 19:13:08 2022

@author: dongdongzheng
"""
from option1 import *
from option2 import *
from option3 import *
from option4 import *

def main():
    import os
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    menu = """
    ***** Vending Machines Manager *****
    1: Add/Edit Machine Profile
    2: Pre-View Sales
    3: Process daily sales
    4: Product Daily sales Analysis
    Q: Quit
    """
    def getOption(prompt):
        while True:
            try:
                retv = input(prompt).strip().upper()
                if retv in ['1','2','3','4',"Q"]:
                    return retv
                    break
                else:
                    print("Invalid option, please enter again")
            except:
                pass
    while True:
        print(menu)
        choice = getOption("Please enter a choice ... ").strip().upper()
        if choice == "1":
            MachineEdit()

        elif choice == "2":
            Pre_sales_view()
            
        elif choice == "3":
            ProcessDailySales("Please enter the date to process [YYYY-MM-DD]: ")
            
        elif choice == "4":
            plottingAnalysis()
            
        elif choice == "Q":
            print("\nThank you for using, Program terminated!")
            print("Goodbye!")
            break
        else:
            print("\nInvalid command, please enter again!")
            
        input("\nPress any key to continue .... ")

if __name__ == "__main__":
    main()