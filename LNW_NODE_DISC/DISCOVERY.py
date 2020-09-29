import mysql.connector
import time
import tkinter as tk

root = tk.Tk ( )
root.title ( "LNW Node Discovery tool" )
canvas = tk.Canvas ( root, height=600, width='800' )
canvas.pack ( )




mydb = mysql.connector.connect(host="10.220.5.126", user='root', passwd='d4NaZ9j3k', database='emsdb')
mycursor = mydb.cursor()
# mycursor.execute('show tables')
# for i in mycursor:
#     print(i)

mycursor.execute('SELECT supportedobjectstr FROM emsdb.htbl_schctp where MOID = "/MA6816023390/SCHCTP=1-A-4-L1-4"')
for i in mycursor:
    supported_obj_list = str(i[0].decode ( 'ascii' )).split(',')
    carrier_list = []
    for item in supported_obj_list:
        if 'CARRIERCTP' in item:
            carrier_list.append(item.split('=')[1])

    # print(i[0].decode('ascii').split(',')[1].split('=')[1])

print(carrier_list)

# time.sleep(5)
print('hi')