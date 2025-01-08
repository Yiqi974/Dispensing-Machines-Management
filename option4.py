#%%
def plottingAnalysis():
    # Importing Packages
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os


    if os.path.exists("SummarySales.csv"):
        #read dataset
        sales = pd.read_csv('SummarySales.csv')
        print('The SummarySales:')
        print(sales.head())
    else:
        print("File not found, please process the pending file first")
        return ;
    
    #data checking 
    def check_data(data):
        print(data.info())
        print('=====================================================================')
        null_columns = data.columns[data.isnull().any()]
        print(data[null_columns].isnull().sum())
        
    # enter year 
    def yr():
        while True:
            try:
                year = input('Please enter the year for analysis [integer]: ').strip()
                year_int = int(year)
                return year
                break
            except:
                print('Invalid input,please enter again!')
    
    #enter month 
    def mon():
        while True:
            try:
                month = input('Please enter the month for analysis: ').strip()
                month_int = int(month)
                if 0 < int(month_int) < 13:
                    return month.zfill(2)
                    break
                else:
                    print('Invalid month, please enter again!')
            except:
                print('Invalid input,please enter again!')
    
    #enter product_ID 
    def prodid():
        while True:
            try:
                Prod_ID = input('Please enter the product ID for analysis: ').strip()
                Prod_ID = Prod_ID.upper()
                return Prod_ID
                break
            except:
                print('Invalid input,please enter again!')
    
    # data-checking
    #print(check_data(sales))
    
    #create yyyy-mm
    sales['date'] = pd.to_datetime(sales['date'],format = '%d/%m/%Y')
    sales['date'] = sales['date'].dt.strftime('%Y%m%d')
    sales['date_ym'] = pd.to_datetime(sales['date'])
    sales['date_ym'] = sales['date_ym'].dt.strftime('%Y%m')
    print('The selected dataset:')
    print(sales.head())
    
    #plotting 
    while True:
        try:
            year = yr()
            month = mon()
            time = year+month
            pid = prodid()
            cond1 = (sales.date_ym == time)
            cond2 = (sales.productId ==pid)
            plot = sales[cond1 & cond2]
            sales_plot = pd.DataFrame(plot.groupby(['date','productId']).Quantity.agg(np.sum)).reset_index()
            if sales_plot.shape[0] >=1:
                print(sales_plot)
                fig = plt.figure(dpi = 300, figsize = (24,12))
                x = sales_plot.date
                y = sales_plot.Quantity
                margin = 0.05
                width = (1-2*margin)/sales_plot.shape[0]
                plt.bar(x = x, height = y, width = 0.3, label = 'Quantity',alpha=0.6)
                for i in range(len(y)):
                    plt.annotate(str(y[i]), xy=(x[i],y[i]), ha='center',va='bottom', fontsize = 18)
                plt.xlabel("Date",fontsize=24)
                plt.ylabel("Sale Quantity",fontsize=24)
                plt.xticks(fontsize=24,rotation = 30)
                plt.yticks(fontsize=24)
                plt.ylim(top = y.max()+4)
                plt.title(label = f'Product Daily Sales Analysis \n(period: {time}; product code: {pid})' ,fontsize=36,pad=40)
                plt.legend(loc = 'best',fontsize = 24)
                plt.show()
                
                again = input('Do you want to continue (Y/N)').strip().upper()
                if again == 'Y':
                    continue
                else:
                    print("Thank You for using")
                    break     
            else:
                again = input('Invalid search, want to continue (Y/N)').strip().upper()
                if again == 'Y':
                    continue
                else:
                    break
 
        except:
            print('Invalid answer, please check the input')
            
                
    

#%%
if __name__ == "__main__":
    plottingAnalysis()

'''
again = input('Do you want to continue (Y/N)').strip().upper()
if again == 'Y':
continue
else:
break
'''
    
    
    
    
