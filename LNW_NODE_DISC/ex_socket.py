import socket
from netmiko import ConnectHandler
from getpass import getpass
import time

install_dir= '/u02/app/karthik/DNA/EMS'

device = {}
remote_host='10.220.5.126'
device['device_type'] = 'cisco_ios_telnet'
device['ip'] = remote_host
device['username'] = 'root'
device['password'] = 'infinera1'
net_connect = ConnectHandler(**device)
time.sleep(2)
print(net_connect.find_prompt())
time.sleep(2)
net_connect.send_command_timing('set length 0')
net_connect.send_command_timing("cd /u02/app/karthik/DNA/EMS/bin")
net_connect.send_command_timing("./ShutDown.sh admin infinera1\n")
output = net_connect.send_command("tail -f ../logs/startup.log", expect_string = r'DNA Server Shutdown successful...')
print(output)
output = net_connect.send_command_timing('\x03')
time.sleep(2)
#output = net_connect.send_command_timing("pwd")
#time.sleep(2)
print(output)

# device = {}
# remote_host='10.220.5.126'
# socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# if socket.connect_ex((remote_host, 23)) == 0:
#     print ('Connection stablished via TELNET')
#     device['device_type'] = 'cisco_ios_telnet'
#     device['ip'] = remote_host
#     device['username'] = 'root'
#     device['password'] = 'infinera2'
#     net_connect = ConnectHandler(**device)
#     socket.close()
# elif socket.connect_ex((remote_host, 22)) == 0:
#     print ('Connection stablished via SSH')
#     device['device_type'] = 'cisco_ios_ssh'
#     device['ip'] = remote_host
#     device['username'] = 'root'
#     device['password'] = 'infinera1'
#     net_connect = ConnectHandler(**device)
#     socket.close()
# else:
#     print ('Unable to connect')
#     socket.close()
# net_connect.disconnect()