import csv
from datetime import *
import tkinter as tk
from tkinter import filedialog
import xlrd

def convert_to_csv(excel_workbook):
    workbook = xlrd.open_workbook(excel_workbook)
    testcase_sheet = workbook.sheet_by_name('testcases')
    with open('C:\Work\R20.0\\temp.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in range ( 119, testcase_sheet.nrows ):

            writer.writerow(testcase_sheet.row_values(row))

#convert_to_csv('C:\Work\R20.0\L0_X_carrier_failure_Testplan.xlsm')
strin = 'C:/Work/R20.0/temp.csv'
path=strin.split('/')
file_name=path[-1].split('.')[0]
pr=''
for i in range(0,len(path)-1):
    pr=pr+path[i]+'/'
pr+=file_name+'.csv'
print(pr)