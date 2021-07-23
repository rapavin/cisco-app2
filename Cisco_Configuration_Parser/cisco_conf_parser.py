import textfsm
import os
import csv
from openpyxl import Workbook
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def cisco_service_parser(reading_running_conf_read_string, checklistOptions):
	# print(checklistOptions)
	global switch_data
	'''Find the location directory of the templates. Currently located at "textfsm_templates"'''
	switch_data = {}
	textfsm_templates_list = os.listdir("/home/ec2-user/webpage/Cisco_Parser/Cisco_Configuration_Parser/textfsm_templates")

	for each_textfsm_templates_list in textfsm_templates_list:
		with open("/home/ec2-user/webpage/Cisco_Parser/Cisco_Configuration_Parser/textfsm_templates/"+each_textfsm_templates_list) as all_textfsm_templates:
			regex_table_fsm_data = textfsm.TextFSM(all_textfsm_templates)
			data = regex_table_fsm_data.ParseText(reading_running_conf_read_string)
			try:
				if len(data)==1:
					switch_data[each_textfsm_templates_list[0:-4]] = data[0]
				elif len(data)==0:
					switch_data[each_textfsm_templates_list[0:-4]] = ["N/A"]
				elif len(data)>1:
					switch_data[each_textfsm_templates_list[0:-4]] = data
			except:
				pass
	wb = Workbook()
	wb.create_sheet("configuration", 0)
	wb.active = 0
	sheet = wb.active
	sheet['A1'] = "HOSTNAME"
	sheet['B1'] = switch_data['cisco_show_run_hostname'][0]
	sheet['A2'] = "SPANNING TREE MODE"
	sheet['B2'] = switch_data['cisco_show_run_spanning_tree_mode'][0]
	sheet['A3'] = "BOOT SYSTEM"
	sheet['B3'] = switch_data['cisco_show_run_boot_system'][0]
	sheet['A4'] = "ENABLE"
	sheet['B4'] = switch_data['cisco_show_run_enable_secret'][0]
	sheet['A5'] = "VTP MODE"
	sheet['B5'] = switch_data['cisco_show_run_vtp_mode'][0]
	sheet['A6'] = "VTp DOMAIN"
	sheet['B6'] = switch_data['cisco_show_run_vtp_domain'][0]
	sheet['A7'] = "DOMAIN NAME"
	sheet['B7'] = switch_data['cisco_show_run_ip_domain_name'][0]
	count = 8

	if "NTP" in checklistOptions:
		if len(switch_data['cisco_show_run_ntp'])>1:
			#sheet['A'+ str(count)] = "\n"
			sheet.insert_rows(count)
			for each_switch_data in switch_data['cisco_show_run_ntp']:
				count = count + 1
				#print('A'+ str(count))
				sheet['A'+ str(count)] = "NTP"
				sheet['B'+ str(count)] = removeExtraSpace(each_switch_data[0])				
				# writer.writerow(["NTP",each_switch_data[0]])
		else:
			pass

	if "AAA" in checklistOptions:
		if len(switch_data['cisco_show_run_aaa'])>1:
			#sheet['A'+ str(count)] = "\n"
			sheet.insert_rows(count+1)
			for each_switch_data in switch_data['cisco_show_run_aaa']:
				count = count + 1
				#print('A'+ str(count+1))
				sheet['A'+ str(count+1)] = "AAA"
				sheet['B'+ str(count+1)] = removeExtraSpace(each_switch_data[0])
				# writer.writerow(["AAA",each_switch_data[0]])
		else:
			pass
		count = count + 1

	if "LOGS" in checklistOptions:
		if len(switch_data['cisco_show_run_logging'])>1:
			# sheet['A'+ str(count)] = "\n"
			sheet.insert_rows(count+2)
			for each_switch_data in switch_data['cisco_show_run_logging']:
				count = count + 1
				sheet['A'+ str(count+1)] = "LOGGING"
				sheet['B'+ str(count+1)] = removeExtraSpace(each_switch_data[0])
		else:
			pass
		count = count + 1
		
	if "CLOCK INFORMATION" in checklistOptions:
		if len(switch_data['cisco_show_run_clock'])>1:
			sheet.insert_rows(count+2)
			for each_switch_data in switch_data['cisco_show_run_clock']:
				count = count + 1
				sheet['A'+ str(count+1)] = "CLOCK INFORMATION"
				sheet['B'+ str(count+1)] = removeExtraSpace(each_switch_data[0])			
		else:
			pass
		count = count + 1
	
	if "SERVICES" in checklistOptions:
		if len(switch_data['cisco_show_run_service'])>1:
			sheet.insert_rows(count+2)
			for each_switch_data in switch_data['cisco_show_run_service']:
				count = count + 1
				sheet['A'+ str(count+1)] = "SERVICES"
				sheet['B'+ str(count+1)] = removeExtraSpace(each_switch_data[0])			
		else:
			pass
		count = count + 1
	
	if "SNMP" in checklistOptions:
		if len(switch_data['cisco_show_run_snmp'])>1:
			sheet.insert_rows(count+2)
			for each_switch_data in switch_data['cisco_show_run_snmp']:
				count = count + 1
				sheet['A'+ str(count+1)] = "SNMP"
				sheet['B'+ str(count+1)] = removeExtraSpace(each_switch_data[0])		
		else:
			pass
		
	sheet.column_dimensions['A'].width = 20
	sheet.column_dimensions['B'].width = 55
	wb.save(os.path.join(BASE_DIR,'TEMP_FILE_STORAGE/interface_testing.xlsx'))

	# with open('/home/ec2-user/webpage/Cisco_Parser/TEMP_FILE_STORAGE/interface_testing.csv', 'w+', newline='') as services_csv_file:
	# 	writer = csv.writer(services_csv_file)
	# 	writer.writerow(["HOSTNAME",switch_data['cisco_show_run_hostname'][0]])
	# 	writer.writerow(["SPANNING TREE MODE",switch_data['cisco_show_run_spanning_tree_mode'][0]])
	# 	#writer.writerow(["VERSION",switch_data['cisco_show_run_version'][0]])
	# 	writer.writerow(["BOOT SYSTEM",switch_data['cisco_show_run_boot_system'][0]])
	# 	writer.writerow(["ENABLE",switch_data['cisco_show_run_enable_secret'][0]])
	# 	writer.writerow(["VTP MODE",switch_data['cisco_show_run_vtp_mode'][0]])
	# 	writer.writerow(["VTP DOMAIN",switch_data['cisco_show_run_vtp_domain'][0]])
	# 	writer.writerow(["DOMAIN NAME",switch_data['cisco_show_run_ip_domain_name'][0]])
	# 	if len(switch_data['cisco_show_run_ntp'])>1:
	# 		writer.writerow([""])
	# 		for each_switch_data in switch_data['cisco_show_run_ntp']:
	# 			writer.writerow(["NTP",each_switch_data[0]])
	# 		else:
	# 			pass
			
	# 	if len(switch_data['cisco_show_run_aaa'])>1:
	# 		writer.writerow([""])
	# 		for each_switch_data in switch_data['cisco_show_run_aaa']:
	# 			writer.writerow(["AAA",each_switch_data[0]])
	# 		else:
	# 			pass
			
	# 	if len(switch_data['cisco_show_run_logging'])>1:
	# 		writer.writerow([""])
	# 		for each_switch_data in switch_data['cisco_show_run_logging']:
	# 			writer.writerow(["LOGGING",each_switch_data[0]])
	# 		else:
	# 			pass
			
	# 	if len(switch_data['cisco_show_run_clock'])>1:
	# 		writer.writerow([""])
	# 		for each_switch_data in switch_data['cisco_show_run_clock']:
	# 			writer.writerow(["CLOCK INFORMATION",each_switch_data[0]])
	# 		else:
	# 			pass
			
	# 	if len(switch_data['cisco_show_run_service'])>1:
	# 		writer.writerow([""])
	# 		for each_switch_data in switch_data['cisco_show_run_service']:
	# 			writer.writerow(["SERVICES",each_switch_data[0]])
	# 		else:
	# 			pass

	# 	if len(switch_data['cisco_show_run_snmp'])>1:
	# 		writer.writerow([""])
	# 		for each_switch_data in switch_data['cisco_show_run_snmp']:
	# 			writer.writerow(["SNMP",each_switch_data[0]])
	# 		else:
	# 			pass	

def removeExtraSpace(word):
	if type(word) is str:
		# print("str")
		if word.endswith(' '):
			word = word[:-1]
			return word
		else:
			return word
	if type(word) is list:
		# print("list")
		for i in word:
			return word.rstrip()

if __name__ == "__main__":
	main()

