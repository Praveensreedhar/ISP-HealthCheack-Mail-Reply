import json
import time
import os
from influxdb import InfluxDBClient
import influxdb
import imaplib
import email
from bs4 import BeautifulSoup
import smtplib
from netmiko import ConnectHandler
from email.mime.text import MIMEText

#os.chdi("C:\\users\\u26928\\Desktop\\SNMP-FLUS-PY_GRA")
os.chdir("/AUTOMATION/LINK-TEST/")
with open('devicestest.json') as dev_file:
	devices = json.load(dev_file)

for device in devices:

    def snmpget(oid):
    
        from pysnmp.entity.rfc3413.oneliner import cmdgen
    
        global SNMP_HOST
        global SNMP_PORT
        global SNMP_COMMUNITY

        SNMP_HOST = device['ip']
        SNMP_PORT = 161
        SNMP_COMMUNITY = 'allyours'
    
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(SNMP_COMMUNITY),
            cmdgen.UdpTransportTarget((SNMP_HOST, SNMP_PORT)),
            oid
        )
    
    # Check for errors and print out results
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
            else:
                for name, val in varBinds:
                    #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                    return val
    download = snmpget(device['oidd'])
    upload = snmpget(device['oidu'])
    hostname = snmpget(device['oidhostname'])
    rpm = snmpget(device['rpm'])
    print(hostname)
    print(download)
    print(upload)
    print(rpm)
    print(device['ip'])
    print(device['oidd'])
    ip_value = device['ip']
    print(ip_value)
    if rpm > 0:
        device = {
            
            'device_type': 'juniper',

            'ip': ip_value,   # Replace with the IP address of your Cisco device

            'username': 'username',

            'password': 'passwd',

                }
        try:

            net_connect = ConnectHandler(**device)
        except Exception as e:
            print(f"Failed to connect to the device: {e}")
            exit()

        try:

            ping_result = net_connect.send_command("ping 10.10.253.173 count 5")
            time.sleep(10)
            print(net_connect.session_log) 
            if "100% packet loss" in ping_result:
           	    

                    print("Ping failed. No response.")
                    print("Please raise a docket with ISP")
        except Exception as e:
                
                print(f"Error executing the ping command: ")
                replay_subject = "TATA 10 MB link Down CKTid:123987"
                reply_message = """
		Hello,
			Please raise a docket with ISP
		Thanks
		Praveen S
		"""                    
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                smtp_username = "abd@gmail.com"
                smtp_password = "xyz"
                sender_email = 'wex@_.com'
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_username, smtp_password)
                    msg = MIMEText(reply_message)
                    msg['Subject'] = reply_subject
                    msg['From'] = smtp_username
                    msg['To'] = sender_email
                    server.sendmail(smtp_username, sender_email, msg.as_string())
                    print("Reply sent successfully.")
        net_connect.disconnect()

    #v = 2000
    #vv = 6000
    #hostname = "TRV-TATA"
    else:
       print(v)
