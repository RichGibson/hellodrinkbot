import os
import shutil
import sqlite3

#location of current database
db_location = '/home/pi/bartendro/ui/bartendro.db'

#Defining list_drink function
def list_drinks():
    import sqlite3
    #connecting to database
    conn = sqlite3.connect(db_location)

    print("Connection opened successfuly!")
    
    #Getting all IDs and Names from drink_name table
    cursor = conn.execute('SELECT id, name FROM drink_name')
    for row in cursor:
       print(row)

#Defining drink_delete function       
def drink_delete():
    import sqlite3
    
    print('\nREMINDER *** Most recent drinks have the highest ID *** REMINDER \n')
    
    #Ask which ID to delete
    drinkid = int(input("What drink ID do you want to delete?"))
    
    #connecting to database
    conn = sqlite3.connect(db_location)

    print("Connection opened successfuly!")
    
    #Delete drink_ID from drink_log table
    cursor = conn.execute('DELETE FROM drink_log WHERE drink_id =?',(drinkid,))
    conn.commit()
    print("Entries Deleted from drink_log")
    
    #Delete drink_ID from drink_booze table
    cursor = conn.execute('DELETE FROM drink_booze WHERE drink_id =?',(drinkid,))
    conn.commit()
    print("Entries Deleted from drink_booze")

    #Delete ID from drink_name table (drinkid variable is the same as id in table)
    cursor = conn.execute('DELETE FROM drink_name WHERE id =?',(drinkid,))
    conn.commit()
    print("Entries Deleted from drink_name")

    #Delete ID from drink table (drinkid variable is the same as id in table)
    cursor = conn.execute('DELETE FROM drink WHERE id =?',(drinkid,))
    conn.commit()
    print("Entries Deleted from drink")

    
    print ("Operation done successfully");
    
    #Closing Connection to database
    conn.close()



#Check is Backup Directory exists, if not create it
if not os.path.exists('/home/pi/bartendro/ui/dbbackup/'):
    os.makedirs('/home/pi/bartendro/ui/dbbackup/')

#Copy DB to backup directory
shutil.copy(db_location, '/home/pi/bartendro/ui/dbbackup/bartendro(0).db')
print('\nDatabase has been copied to backup folder \n')

#Calling list_drink function
list_drinks()

#Calling drink_delete function
drink_delete()

