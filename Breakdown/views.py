from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from Interface_Cisco_Configuration_Parser import interface_ciscoconfparse
from Cisco_Configuration_Parser import cisco_conf_parser
from pathlib import Path
import requests
import csv
import os
import traceback
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

def Home_Page(request):
    return render(request, 'base.html')

def Cisco_Parser_Page(request):
    return render(request, 'Cisco_Parser_Page.html')

def Network_Page(request):
    return render(request, 'Network_Page.html')

def delete_file():
    os.remove(os.path.join(BASE_DIR,'TEMP_FILE_STORAGE/interface_testing.xlsx'))
    # os.remove('/home/ec2-user/webpage/Cisco_Parser/TEMP_FILE_STORAGE/interface_testing.csv')

def convert_each_uploaded_file_readlines_to_string(list_variable):
    str1 = "" 
    for each_running_configuration_list in list_variable: 
        str1 += each_running_configuration_list
        str1 += "\n"
    return str1

def upload_read(request):
    global running_configuration_list
    running_configuration_list = []
    try:
        checklistOptions = request.POST.getlist('checklist[]')
        # print(checklistOptions)
        f = request.FILES['running_config']
        if "." in f.name[-4]:
            hostname = f.name[0:-4]
        elif "." in f.name[-5]:
            hostname = f.name[0:-5]
        uploaded_file_readlines_list = request.FILES['running_config'].readlines()
        #print(uploaded_file_readlines_list)
        for each_uploaded_file_readlines in uploaded_file_readlines_list:
            running_configuration_list += [each_uploaded_file_readlines.decode().strip("\n").strip("\r")]
        running_configuration_list_read = convert_each_uploaded_file_readlines_to_string(running_configuration_list)
        cisco_conf_parser.cisco_service_parser(running_configuration_list_read, checklistOptions)
        final_config = interface_ciscoconfparse.main(running_configuration_list, checklistOptions)

        with open(os.path.join(BASE_DIR,'TEMP_FILE_STORAGE/interface_testing.xlsx'), 'rb') as fq_read_bytes:
            data_bytes = fq_read_bytes.read()
        
        response = HttpResponse(data_bytes, content_type='text/html; charset=UTF-8')
        response['Content-Disposition'] = 'attachment; filename='+hostname+'.xlsx'
        delete_file()
        return response
        return render(request, 'Parser_Page.html')
    except Exception:
        return render(request, 'Parser_Page.html')
