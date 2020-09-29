from collections import deque
import csv
from datetime import *
import tkinter as tk
from tkinter import filedialog
import mysql.connector
from Carrier import *
import json
from Deserialization_example import *

# root = tk.Tk ( )
# root.title ( "JSON Creator" )
# canvas = tk.Canvas ( root, height=600, width='800' )
# canvas.pack ( )
#
# frame = tk.Frame ( root, bd='5', bg='#bfff00' )
# frame.place ( relx=0.5, rely='0.1', relwidth=0.9, relheight=0.05, anchor='n' )
#
# Input_file_path = tk.Entry ( frame )
# Input_file_path.place ( relwidth=0.75, relheight=1 )
#
# submit_button = tk.Button ( frame, text='Submit', command=lambda: create_JSON ( Input_file_path.get ( ) ) )
# submit_button.place ( relx=0.76, relheight=1, relwidth=0.1 )
#
# browse_button = tk.Button ( frame, text='Browse...', command=lambda: browse_file ( ) )
# browse_button.place ( relx=0.87, relheight=1, relwidth=0.1 )
#
# Output_frame = tk.Frame ( root, bd=5, bg='#ff8c1a' )
# Output_frame.place ( relx=0.5, rely=0.5, relwidth=0.9, relheight=0.2, anchor='n' )
#
# # output_box = tk.Label(Output_frame, font = 18 )
# # output_box.place(relwidth = 1,  relheight = 0.6)
#
# output_box = tk.Text ( Output_frame, font=18 )
# output_box.place ( relwidth=1, relheight=0.6 )
#
# close_button = tk.Button ( Output_frame, text='Close', command=lambda: close_dialog ( ) )
# close_button.place ( relx=0.5, relheight=0.25, rely=0.7, relwidth=0.08 )
#
# def close_dialog ( ):
#     root.destroy ( )

# def browse_file ( ):
    # root2 = tk.Tk()
    # root2.withdraw()
    # root.withdraw()
    # Input_file_path.delete ( 0, "end" )
    # file_path_explored = filedialog.askopenfile ( initialdir="C:\\", title='Select OCLR trace export file' )
    # root2.destroy()
    # print(file_path_explored.name)
    # Input_file_path.insert ( 0, file_path_explored.name )

def create_JSON(oclr_trace):
    #oclr_trace = 'C:\Work\R20.0\Setup2\OCLR.tsv'
    now = datetime.now ( )
    path = oclr_trace.split ( '/' )
    file_name = path[-1].split ( '.' )[0]
    final_file = ''
    for i in range ( 0, len ( path ) - 1 ):
        final_file = final_file + path[i] + '/'
    final_file += file_name + str ( datetime.timestamp ( now ) ) + '.txt'
    with open(oclr_trace, 'r') as oclr_file:
        tmp_reader = csv.reader(oclr_file, delimiter = '\t')
        # i = iter(tmp_reader)
        # print(len(i))
        for i in range(14):
            next(tmp_reader)
        Src = next(tmp_reader)

        oxcons_list = dict()
        for line in tmp_reader:
            if 'Optical Cross-Connect' in line:
                oxcons_list[f"{line[4]}_{line[8]}"] = {0 : line[4] , 'aid' :  line[8]}



    with open(oclr_trace, 'r') as oclr_file:
        x=deque ( csv.reader ( oclr_file, delimiter = '\t' ), 1 )[0]
        DstSchAid = x[8]
        DstNodeName = x[4]
    #print(oxcons_list )


    mydb = mysql.connector.connect ( host=DNA_IP, user=DNA_DB_USERNAME, passwd=DNA_DB_PASSWD, database='emsdb' )
    mycursor = mydb.cursor ( )
    for key in oxcons_list.keys():
        frm_aid = oxcons_list[key]['aid'].split('%')[1][0:5]
        #print(frm_aid)
        # print(frm_aid)
        mycursor.execute ( f'select HIBNODEID from emsdb.htbl_toponode where MENAME =  "{oxcons_list[key][0]}" ' )
        for i in mycursor:
            # print(i[0].decode())
            oxcons_list[key]['node_id'] = i[0].decode()
            # print(oxcons_list)
            oxcons_list[key]['moid'] = f'/{oxcons_list[key]["node_id"]}/OPTICAL_XCON={oxcons_list[key]["aid"]}'
            mycursor2 = mydb.cursor()
            mycursor2.execute(f'select OPERATINGMODE from emsdb.htbl_frm where MOID =  "/{i[0].decode()}/FRM={frm_aid}" ' )
            for x in mycursor2:
                # print("\n"+x[0])
                if 'native' in x[0].decode().lower():
                    oxcons_list[key]['op'] = 'Native'
                else:
                    oxcons_list[key]['op'] = 'SLTE'
    #print(oxcons_list)
    TerrestrialPath= []
    SltePath = []
    for key in oxcons_list.keys():
        if oxcons_list[key]['op'] == 'Native':
            TerrestrialPath.append(Oxcon(oxcons_list[key][0], oxcons_list[key]['aid'], oxcons_list[key]['node_id'] , oxcons_list[key]['moid']))
        else:
            SltePath.append(protected_oxcon(oxcons_list[key][0], oxcons_list[key]['aid'], oxcons_list[key]['node_id'] , oxcons_list[key]['moid']))


    SrcSchAid = Src[8]

    SrcNodeName = Src[4]
    #print(Src, DstSch)

    mycursor.execute ( 'select HIBNODEID from emsdb.htbl_toponode where MENAME =  ' + f'"{SrcNodeName}" ' )
    for i in mycursor:
        SrcNodeId = str ( i[0].decode ( 'ascii' ) )

    SrcSchMoid = f'/{SrcNodeId}/SCHCTP={SrcSchAid}'

    SrcSch = SchCtp(SrcSchMoid, SrcSchAid, SrcNodeId, SrcNodeName)
    mycursor.execute ( 'select HIBNODEID from emsdb.htbl_toponode where MENAME =  ' + f'"{DstNodeName}" ' )
    for i in mycursor:
        DstNodeId = str ( i[0].decode ( 'ascii' ) )

    DstSchMoid = f'/{DstNodeId}/SCHCTP={DstSchAid}'
    DstSch = SchCtp(DstSchMoid, DstSchAid, DstNodeId, DstNodeName)

    SchList = [SrcSch,DstSch]
    data = dict()

    data = {
        "optical_services": [
            {
                "subsea_path": {
                    "protected_oxcon": [ x.data for x in SltePath]
                },
                "terrestrial_path": {
                    "oxcons": [ z.data for z in TerrestrialPath]
                },
                "name": "workOs",
                "superchannels" : [ s.data for s in SchList],
                "operational_state": None,
                "lifecycle_state": None
            }

        ]
    }
    data_json = json.dumps(data, indent=2)
    # print(data)
    print(data_json)






create_JSON(OCLR_trace_file)

#root.mainloop ( )