from libs import *

def new_writer(dictionary_list,desired_header,color_scheme = 0, custom_data = False):
    color_schemes = {
        0: [bg.blue,bg.cyan],
        1: [bg.blue,bg.white],
        2: [bg.blue,bg.magenta],
        3: [bg.green,bg.blue],
        4: [bg.green,bg.white],
        5: [bg.magenta,bg.white],
        6: [bg.cyan,bg.green],
        7: [bg.cyan,bg.magenta],
        8: [bg.cyan,bg.white],
        9: [bg.green,bg.magenta]
    }

    col_width = []

    for header in desired_header:
        col_width.append(len(header))

    rows = []
    #import a list of dictionaries and unpack
    for data_dict in dictionary_list:

        #find column width and append data to row
        row = []
        for num,val in enumerate(list(data_dict.values())):

            current_width = len(str(val))
            row.append(val)
            if current_width > col_width[num]:
                col_width[num] = current_width
        rows.append(row)
            
    #print the table

    #header
    for col,data in enumerate(dictionary_list):
        width = col_width[col]
        set_font(text.bold,text.underline)
        print(f' {desired_header[col]:<{width}}|',end="")
        reset()

    print()

    row_num = 1
    for row in rows:
        if is_even(row_num):
            color = set_font(color_schemes[color_scheme][0])
        else:
            color = set_font(color_schemes[color_scheme][1])

        col_num = 0
        while col_num < len(desired_header):
            color
            width = col_width[col_num]
            print(f" {row[col_num]:<{width}}|",end='')
            col_num += 1
        
        reset()
        print()
        row_num += 1

    print()
    #print table


def table_writer(dataset_list,column_names_dict = False, color_scheme = 0):

    color_schemes = {
        0: [bg.blue,bg.cyan],
        1: [bg.blue,bg.white],
        2: [bg.blue,bg.magenta],
        3: [bg.green,bg.blue],
        4: [bg.green,bg.white],
        5: [bg.magenta,bg.white],
        6: [bg.cyan,bg.green],
        7: [bg.cyan,bg.magenta],
        8: [bg.cyan,bg.white],
        9: [bg.green,bg.magenta]
    }

    col_width_dict = {}

    rows = []
    #import a list of dictionaries and unpack
    for data_dict in dataset_list:

        #find column width
        header = list(data_dict.keys())
        row = []
        for col,val in data_dict.items():
        
            try:
                col_width_dict[col] = max(len(col), len(str(val)), col_width_dict[col])

            except:
                col_width_dict[col] = max(len(col), len(str(val)))

            row.append(val)

        #prepare data for print
        rows.append(row)

    num_rows = len(rows)
    print('\n' * (num_rows),flush=True)

    move_cursor(num_rows,'u')    

    #print first column's header first
    for col_num, col_name in enumerate(header):
        row_num = 0

        #set column width:
        width = col_width_dict[col_name]+2
        
        #set header style, and print column name
        set_font(text.bold, text.underline, bg.black)
        print(f'{col_name:<{width}} |', end = '',flush=True)

        reset()

        #print one column at a time until all data is done
        while row_num < num_rows:
            row = rows[row_num]
            if is_even(row_num):
                color = set_font(color_schemes[color_scheme][0])
            else:
                color = set_font(color_schemes[color_scheme][1])
            row_num += 1
            
            move_cursor(1,'d')
            move_cursor(width+2,'l')
            
            color
            print(f'{row[col_num]:<{width}} |', end = '',flush=True)
            reset()

        move_cursor(row_num, 'u')

    if col_num == len(header)-1:
        print('\n' * (num_rows+2),flush=True)

    def new_writer(dictionary_list,desired_header,custom_data = False):

        col_width_dict = {}
        col_width_list = []

        for header in desired_header:
            col_width_list.append(len(header))

        
        #import a list of dictionaries and unpack
        for data_dict in dictionary_list:

            #find column width
            for num,col,val in enumerate(data_dict.items()):

                current_width = max(col,val)

                if current_width > len(col_width_list[num]):
                    col_width_list[num] = current_width
                
        #print header
        for i,header in enumerate(desired_header):
            print(f' {header:<{col_width_list[i]}}|')

        #print table

        for i,data in enumerate(dictionary_list):
            print(f' {data:<{col_width_list[i]}}|')

