import csv
from datetime import *



def convert_to_text(input_file_path):
    now=datetime.now()
    final_file = input_file_path.split('.')[0] + '_'+str(datetime.timestamp(now))+'.txt'
    with open(input_file_path, 'r') as carrier:
        tmp_reader = csv.reader(carrier)


        with open(final_file, 'w', newline='') as template_file1:

            tmp_writer1=csv.writer(template_file1, delimiter = ';')
            test=[]
            test.clear()
            for line in tmp_reader:
                test.clear ( )
                for item in line[0:21]:
                    test.append("'"+item+"'")
                temp=test[9]
                print(temp)
                tmp_writer1.writerow(test)
    output_box['text'] = final_file


