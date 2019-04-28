# Attendance-Data-Processing
Attendance Data Processing using PANDA

Considered :
 1. Sample Excel Sheet is added. It should have three data like below 
    Awais;"2018-11-20 01:00:19";0   # Name;Date; Punch > punch 0 for chekin and One for check out
    Awais;"2018-11-20 05:00:19";1   # Name;Date; Punch > punch 1 for check out
    
 2.If multiple entries for chekin is there for a single day then consider earliest one.
 
 3.If multiple entries for check-out then considered last one.
 
 4. If there is only one chekin for a day and there is no chek out and there is chekout next day
