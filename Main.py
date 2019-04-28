import pandas as pd 
import numpy as np

def str_to_dt(radardetails):
    return  radardetails.strip('\"')

def main():
    readExcelFile()
    pass

def readExcelFile():  
    ExcelPath = "Attendance.xlsx"
    # reading csv file  
    df =pd.read_excel(ExcelPath,sheet_name='Sheet1')  
    # segregate columns :One COlumn data to three column   
    df[['Name', 'DateTime', 'Punch']] = df['name;"pyzk_datetime";"pyzk_punch"'].str.split(';', expand=True) 
    # Delete the "Area" column from the dataframe
    df = df.drop('name;"pyzk_datetime";"pyzk_punch"', axis=1)
    # change data type
    df['DateTime'] = df['DateTime'].apply(str_to_dt) 
    #Shorting Accordingly
    df.sort_values(by=['Name', 'DateTime'],ascending=True,inplace=True)
    #newColumn Added in DataFrame
    df['OnlyDate']=pd.DatetimeIndex(df['DateTime']).date    
    dropduplicate(df)
    pass

def dropduplicate(df):
#     one Checkout and one chekin record for each date
    checkout_df = df[df['Punch']=='1'].drop_duplicates(subset=['Name','OnlyDate'], keep='last')
    checkin_df = df[df['Punch']=='0'].drop_duplicates(subset=['Name','OnlyDate'], keep='first')
    df = checkin_df.append(checkout_df, ignore_index=True)
    df.sort_values(by=['Name', 'DateTime','Punch'],ascending=True,inplace=True)
    df =checkin_df.merge(checkout_df, on=['Name','OnlyDate'],how='outer',suffixes=['_checkin', '_checkout'])[['Name','OnlyDate','DateTime_checkin','DateTime_checkout']]
    df["DateTime_checkout"]= pd.to_datetime(df["DateTime_checkout"]) 
    df["DateTime_checkin"]= pd.to_datetime(df["DateTime_checkin"])
    PreProcess(df)
    pass

def PreProcess(df):
    final = df.sort_values(by=['Name', 'OnlyDate'],ascending=True).reset_index(drop=True)
    for i in range(0, len(final)):
        if final.isnull().loc[i, 'DateTime_checkout']:           
            if i < len(final)-1:
                final.loc[i, 'DateTime_checkout'] = final.loc[i+1, 'DateTime_checkout']
        pass
    final['TotalTime']=final['DateTime_checkout'].values-final['DateTime_checkin'].values
    dropMoreThen15Hours(final)
    pass
def dropMoreThen15Hours(final):
    final['TimeOut'] = final.apply(lambda x: 'Y'  if x['TotalTime'].total_seconds()/(3600.0) > 15  else  'N' , axis=1)
    print(final.head(100))     
    pass
    

if __name__ == "__main__": 
    main()
