import xlsxwriter
import netmiko
import ciscoconfparse

# connect to a device
def connect(device,username,password):
	return netmiko.ConnectHandler(device_type='cisco_wlc_ssh',ip=device,username=username,password=password)

# figure out controller type
def get_controller_type(controller_ip_addr):
	return True

# read information for workbook from controller, writes backup to file system, then imports into ciscoconfparse
def controller_read(wlc_netmiko_obj,file_name,password):
	out1 = wlc_netmiko_obj.send_command_expect("config passwd-cleartext enable","assword:")
	print(out1)
	wlc_netmiko_obj.send_command(password)
	wlc_netmiko_obj.send_command("config switchconfig secret-obfuscation disable")
	conf = wlc_netmiko_obj.send_command("show run-config commands")
	with open(file_name, "w") as f:
		f.write(conf)
	parse = ciscoconfparse.CiscoConfParse(file_name)
	return parse

#write information from contoller to spreadsheet template
def document_write(file_name):
	return True

def main():
	wlc_ip_addr = raw_input("Enter Controller Managent IP address : ")
	username = raw_input("Enter Controller Admin username : ")
	password = raw_input("Enter Controller Management password : ")
	wlc = connect(wlc_ip_addr,username,password)
	config = controller_read(wlc,"config.txt",password)
	for obj in config.find_objects(r"user"):
		print(obj.text)
	

if __name__ == "__main__":
	main()
