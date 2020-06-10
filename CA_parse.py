###########################################################################################################################################
#                                                                                                                                        #
#  Name: CA Dynamic Testing                                                                                                              #                                                                                                        #                                   
#  Takes CA_Interface_sheet.csv as input and generates CA_Out.csv                                                                        #
#  CA_Out.csv contains signals, datatype, min_value,max_value,read,write,source and line numbers data                                    #
#                                                                                                                                        #
#                                                                                                                                        #
###########################################################################################################################################






import csv
import linecache
import os

IW_signals_list = []
data = {}
min_max_dict = {}
MMC1_signals_list,IM_signals_list,VS_signals_list,ACC_signals_list,LC_signals_list = [], [] , [] , [] , []




CA_SRC = "..\\..\\Autocode\\Autocode\\CA\\CtAp_AptivCA.c"

ACC  =   "..\\..\\Autocode\\Autocode\\ACC\\CtAp_AptivACC.c"
IW   =   "..\\..\\Autocode\\Autocode\\IW\\CtAp_AptivIW.c"
IM   =   "..\\..\\Autocode\\Autocode\\IM\\CtAp_AptivIM.c"
VS   =   "..\\..\\Autocode\\Autocode\\VS\\CtAp_AptivVS.c"
LC   =   "..\\..\\Autocode\\Autocode\\LC\\CtAp_AptivLC.c"
MMC1 =   "..\\..\\Autocode\\Autocode\\MMC1\\"


def finditer_with_line_numbers(pattern, string, flags=0):
    '''
    A version of 're.finditer' that returns '(match, line_number)' pairs.
    function inputs are (pattern, string, flags=0)
    outputs is a iter which has re.match object and int - line number pair. 
    '''
    import re

    matches = list(re.finditer(pattern, string, flags))
    if not matches:
        return []

    end = matches[-1].start()
    # -1 so a failed 'rfind' maps to the first line.
    newline_table = {-1: 0}
    for i, m in enumerate(re.finditer(r'\n', string), 1):
        # don't find newlines past our last match
        offset = m.start()
        if offset > end:
            break
        newline_table[offset] = i

    # Failing to find the newline is OK, -1 maps to 0.
    for m in matches:
        newline_offset = string.rfind('\n', 0, m.start())
        line_number = newline_table[newline_offset]
        yield (m, line_number)

def find_my_str(str_data, file_input_str, any_other_str=''):
    '''
    function to find last update of var in the file 
    --------------------------------------------------------------------------
    i/p :
    str_data        = variable name 
    file_input_str  = String of file which is to be used for searching
    any_other_str   = any extra string or structure name you want to give (optional)
    -------------------------------------------------------------------------------
    o/p:
    var_name        = variable name with structure
    line number     = int  
    '''
    #with open(file_input) as FH :
    pattern_1 = r'(\b.*'+any_other_str+r'.*'+str_data+r')[\s\n]*='
    data_1 = finditer_with_line_numbers(pattern_1,file_input_str)
    try:
        last_string = list(data_1)[-1]
        var_name = last_string[0].group(1)
        line_num = last_string[1]
    except IndexError:
        print(data_1)
        var_name = 'Not Found'
        line_num = -2
    return var_name,line_num+1


def get_signals_from_csv():
    with open(r'CA_Interface_sheet.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader)
        if header!= None:
            for row in csv_reader:
                if row[5] == "IW":
                    if len(row[0].split(".")) == 3:
                        signal_start = row[0].find(".") + 1
                        act_signal_tofind = row[0][signal_start:]
                    else:
                        act_signal_tofind = row[0]
                    if act_signal_tofind not in IW_signals_list:
                        IW_signals_list.append(act_signal_tofind)
                        data[act_signal_tofind] = row[0]
                        min_max_dict[act_signal_tofind] = row[2],row[6],row[7]
                if row[5] == "IM":
                    signal_start = row[0].find(".") + 1
                    act_signal_tofind = row[0][signal_start:]
                    if act_signal_tofind not in IM_signals_list:
                        IM_signals_list.append(act_signal_tofind)
                        data[act_signal_tofind] = row[0]
                        min_max_dict[act_signal_tofind] = row[2],row[6],row[7]
                if row[5] == "VS":
                    signal_start = row[0].find(".") + 1
                    act_signal_tofind = row[0][signal_start:]
                    if act_signal_tofind not in VS_signals_list:
                        VS_signals_list.append(act_signal_tofind)
                        data[act_signal_tofind] = row[0]
                        min_max_dict[act_signal_tofind] = row[2],row[6],row[7]
                if row[5] == "ACC":
                    signal_start = row[0].find(".") + 1
                    act_signal_tofind = row[0][signal_start:]
                    if act_signal_tofind not in ACC_signals_list:
                        ACC_signals_list.append(act_signal_tofind)
                        data[act_signal_tofind] = row[0]
                        min_max_dict[act_signal_tofind] = row[2],row[6],row[7]           
                if row[5] == "LC":
                    signal_start = row[0].find(".") + 1
                    act_signal_tofind = row[0][signal_start:]
                    if act_signal_tofind not in LC_signals_list:
                        LC_signals_list.append(act_signal_tofind)
                        data[act_signal_tofind] = row[0]
                        min_max_dict[act_signal_tofind] = row[2],row[6],row[7]
                if row[5] == "MMC1":
                    signal_start = row[0].find(".") + 1
                    act_signal_tofind = row[0][signal_start:]
                    if act_signal_tofind not in MMC1_signals_list:
                        MMC1_signals_list.append(act_signal_tofind)
                        data[act_signal_tofind] = row[0]
                        min_max_dict[act_signal_tofind] = row[2],row[6],row[7]
read_data = {}
index = {}

def to_get_index():
    count = 0
    for k in read_data.keys():
        count = count + 1 
        index[k] = count

def get_read_data(CA_SRC, signals):
    for signal in signals:
        with open(CA_SRC) as my_file:
            for num,line in enumerate(my_file,1):
                if signal in line:
                    line_number = num - 1
                    exact_line = linecache.getline(CA_SRC,line_number)
                    exact_line = exact_line.strip()
                    if len(signal.split(".")) == 2:
                        signal_split_1 = signal.split(".")[1]
                    else:
                        signal_split_1 = signal
                    if signal_split_1 in exact_line:
                        string_read = exact_line.strip("=")
                        if "(Rte_IRead_" in string_read:
                            string_read = exact_line.split("=")[0]
                        read_data[signal] = string_read,line_number
                        found = 1
                        break
                
                    


def export():
    with open('CA_Out.csv','w',newline='') as output:
        cw = csv.writer(output)
        cw.writerow(["Index","Reciever_Port_Name","Write_data_type","Min_Value","Max_Value","Filename","Readport_Variable", "Readport_lineNumber","Writeport_Variable", "Writeport_lineNumber"])
        for k in read_data.keys():
            cw.writerow([index[k],data[k],min_max_dict[k][0],min_max_dict[k][1],min_max_dict[k][2],write_data[k][0],read_data[k][0],read_data[k][1],write_data[k][1],write_data[k][2]])


write_data = {}

def get_write_port_variable_and_line_number(source_file,signals_source):
    for signal in signals_source:
        found = 0
        with open(source_file) as my_file:
            for num,line in enumerate(my_file,1):
                if "IW" in source_file:
                    if signal in line:
                        count =  source_file.find("CtAp")
                        src = source_file[count:]
                        string_write_var = line.strip().split("=")[0].strip().replace("->",".")
                        write_data[signal] = src, string_write_var,num
                        found = 1
                if "IM" in source_file:
                    if signal in line:
                        count =  source_file.find("CtAp")
                        src = source_file[count:]
                        string_write_var = line.strip().split("=")[0].strip().replace("->",".")
                        write_data[signal] = src, string_write_var,num
                        found = 1


def get_write_port_variable_and_line_number_updated(source_file,signals_source):
        with open(source_file) as my_file:
            file_data = my_file.read()
            #for num,line in enumerate(my_file,1):
            if "IW" in source_file or "IM" in source_file:
                for signal in signals_source:
                    found = 0
                    print(signal)
                    s_name, line_number_temp = find_my_str(signal.strip().replace("->",".").split('.')[-1],file_data, any_other_str = '')
                    string_write_var = s_name.strip().replace("->",".")
                    src = string_write_var.split('.')[0]
                    write_data[signal] = src, string_write_var, line_number_temp
                    found = 1
            # if "IM" in source_file:
            #     for signal in signals_source:
            #         found = 0
            #         if signal in line:
            #             count =  source_file.find("CtAp")
            #             src = source_file[count:]
            #             string_write_var = line.strip().split("=")[0].strip().replace("->",".")
            #             write_data[signal] = src, string_write_var,num
            #             found = 1



def clear():
    IM_signals_list.clear()
    MMC1_signals_list.clear()
    LC_signals_list.clear()
    VS_signals_list.clear()
    IW_signals_list.clear()
    ACC_signals_list.clear()


def main():
    get_signals_from_csv()
    get_read_data(CA_SRC,IM_signals_list)
    to_get_index()
    #get_write_port_variable_and_line_number(IW,data.keys())
    #get_write_port_variable_and_line_number(IM,data.keys())
    get_write_port_variable_and_line_number_updated(IM,data.keys())
    export()
    clear()

if __name__ == "__main__":
    main()






'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Revision Log

 Date      By         JIRA Issue / Change Description
 --------- ---------- -------------------------------------------------------------------------------------------------------------------------------------------

 09-06-2020 Dhanush   Initial creation
					  Script is Able to generate CA_Out.csv containg read data and write data for Aptiv_IW Provider for CA
 
                      
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                   