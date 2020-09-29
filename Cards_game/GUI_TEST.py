import csv
from datetime import *
import tkinter as tk
from tkinter import filedialog
import xlrd
import tkinter.scrolledtext as scrolledtext


root = tk.Tk ( )
root.title ( "Devtest file creator" )
canvas = tk.Canvas ( root, height=600, width='800' )
canvas.pack ( )

frame = tk.LabelFrame ( root, bd='5', bg='#bfff00' , text = "Enter your testplan path below and click on Submit:\t" , font = 14)
frame.place ( relx=0.5, rely='0.03', relwidth=0.9, relheight=0.12, anchor='n' )

Input_file_path = tk.Entry ( frame )
Input_file_path.place ( relwidth=0.75, relheight=0.6 )

submit_button = tk.Button ( frame, text='Submit', command=lambda: convert_to_text ( Input_file_path.get ( ) ) )
submit_button.place ( relx=0.87, relheight=0.6, relwidth=0.1 )

browse_button = tk.Button ( frame, text='Browse...', command=lambda: browse_file ( ) )
browse_button.place ( relx=0.76, relheight=0.6, relwidth=0.1 )


Log_frame = tk.LabelFrame ( root, bd=5, bg='#f0d56c', text = "Errors/Warnings :\t" , font = 14)
Log_frame.place( relx=0.5, rely=0.2, relwidth=0.9, relheight=0.45, anchor='n' )

Log_box = scrolledtext.ScrolledText(Log_frame)
Log_box['font'] = ('consolas', '12')
Log_box.place(relwidth=0.99, relheight=0.95)


Output_frame = tk.LabelFrame ( root, bd=5, bg='#ff8c1a', text = "Result text file :\t", font = 14 )
Output_frame.place ( relx=0.5, rely=0.75, relwidth=0.9, relheight=0.2, anchor='n' )

output_box = tk.Text ( Output_frame, font=18 )
output_box.place ( relwidth=1, relheight=0.6 )



close_button = tk.Button ( Output_frame, text='Close', command=lambda: close_dialog ( ) )
close_button.place ( relx=0.5, relheight=0.25, rely=0.7, relwidth=0.08 )


def convert_to_text ( input_file_path ):
    now = datetime.now ( )
    path = input_file_path.split ( '/' )
    file_name = path[-1].split ( '.' )[0]
    final_file = ''
    for i in range ( 0, len ( path ) - 1 ):
        final_file = final_file + path[i] + '/'
    final_file += file_name + str ( datetime.timestamp ( now ) ) + '.txt'
    workbook = xlrd.open_workbook ( input_file_path )
    testcase_sheet = workbook.sheet_by_name ( 'testcases' )


    with open ( final_file, 'w', newline='' ) as template_file1:

        tmp_writer1 = csv.writer ( template_file1, delimiter=';' )
        test = []
        test.clear ( )
        start_row = 120
        Log_box.insert ( tk.END,
                         "Below Errors/Warnings were found in your testplan. You can correct them in your test plan and re-run the tool\n\n" )
        for line in range ( 119,testcase_sheet.nrows ):
            line2 = testcase_sheet.row_values(line)
            test.clear ( )
            for item in line2[0:21]:
                if ';' in item:
                    item = item.replace(';', ' ')
                if '"' in item:
                    item = item.replace('"', ' ')
                if "'" in item:
                    item = item.replace("'", ' ')

                test.append ( "'" + item + "'" )
            if test == ["''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''", "''"]:
                continue

            if test[0] == "''" :
                Log_box.insert ( tk.END, "IFN is empty in " + str(start_row) + " row\n")
            if test[1] == "''":
                Log_box.insert ( tk.END, "RF1 is empty in " + str(start_row) + " row\n")
            if test[7] == "''":
                Log_box.insert ( tk.END, "Testcase title is empty in " + str(start_row) + " row\n")
            if test[9] == "''":
                Log_box.insert ( tk.END, "Test Case Owner is empty in " + str(start_row) + " row\n")
            if test[10] == "''":
                Log_box.insert ( tk.END, "Feature is empty in " + str(start_row) + " row\n")
            if test[12] == "''":
                Log_box.insert ( tk.END, "Priority is empty in " + str(start_row) + " row\n")
            if test[13] == "''":
                Log_box.insert ( tk.END, "Req No is empty in " + str(start_row) + " row\n")
            if test[15] == "''":
                Log_box.insert ( tk.END, "Release Introduced is empty in " + str(start_row) + " row\n")
            if test[16] == "''":
                Log_box.insert ( tk.END, "Management Interface is empty in " + str(start_row) + " row\n")
            if test[17] == "''":
                Log_box.insert ( tk.END, "Product is empty in " + str(start_row) + " row\n")
            if test[20] == "''":
                Log_box.insert ( tk.END, "Is Automatable is empty in " + str(start_row) + " row\n")

            tmp_writer1.writerow ( test )
            start_row=start_row+1

    output_box.insert ( 0.0, 'Result file\t:\t' + final_file )


def browse_file ( ):
    Input_file_path.delete ( 0, "end" )
    file_path_explored = filedialog.askopenfile ( initialdir="C:\\", title='Select Test plan file' )
    Input_file_path.insert ( 0, file_path_explored.name )


def close_dialog ( ):
    root.destroy ( )

root.mainloop ( )
