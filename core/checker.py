# Router interface: 192.168.202.1
# Windows interface: 192.168.202.1
# Linux interface: 192.168.202.3
# Project files: /home/user/checker
from easysnmp import Session
from datetime import timedelta
import re
import os
import time
import datetime as czas


class Checker():
    def __init__(self, host):
        if host[5] == '2' or host[5] == '2c':
            self.session = Session(hostname=host[4], version=2, community=host[6])
        elif host[5] == '3':
            self.session = Session(hostname=host[4], version=3, security_username=host[7], security_level=host[8],
                                   privacy_protocol=host[9], privacy_password=host[10], auth_protocol=host[11],
                                   auth_password=host[12])

    def uptime(self):
        snmp_get = self.session.get('1.3.6.1.2.1.1.3.0')
        hundredths_sec = int(snmp_get.value)
       # print(hundredths_sec)
        # sec = int((hundredths_sec / 100) % 60)
        # min = int((hundredths_sec / (100 * 60)) % 60)
        # hours = int((hundredths_sec / (100 * 60 * 60)) % 24)
        # result = "%02d:%02d:%02d" % (hours, min, sec)
        date = timedelta(microseconds=hundredths_sec*1e4)
        result = str(date).split(".")[0]
        return result

    def ping(self, ipaddress):
        # data = subprocess.check_output("ping " + str('192.168.202.1') + " -c 1")
        data = os.popen("ping " + ipaddress + " -n 1").read()
        time.sleep(1)
        data = str(data)
        #return data

        # res = subprocess.call(['ping', '-c', '3', address])
        # if res == 0:
        #     print
        #     "ping to", address, "OK"
        # elif res == 2:
        #     print
        #     "no response from", address
        # else:
        #     print
        #     "ping to", address, "failed!"
        if "ttl" in data:
            result = re.findall('[0-9]+ms', data)
            return result[-1]
        else:
            data = re.search('from [0-9.: ]+[A-z ]+', str(data)).group().replace("from ", "")
            for_delete = re.search('[0-9.]+: ', data).group()
            result = data.replace(for_delete, "")
            return result
       # except Exception as err:
           # print("error")
            # error = Statements()
            # return error.get_statement(err)

    def interface_select(self, interface):
        interfaces = []
        items = self.session.walk('1.3.6.1.2.1.2.2.1.2')
        for item in items:
            interfaces.append(item.value)
        if interface in interfaces:
            if_index = interfaces.index(interface)+1
            return if_index
        else:
            return 0

    def interface_status(self, interface):
        if_index = self.interface_select(interface)

        if if_index == 0:
            return "Interface not found"
        oid = '1.3.6.1.2.1.2.2.1.8.' + str(if_index)
        snmp_get = self.session.get(oid)
        number = snmp_get.value
        status = {
            1: "Up",
            2: "Down",
            3: "Testing",
            4: "Unknown",
            5: "Dormant",
            6: "Not present",
            7: "Lower layer down"
        }
        status = status.get(int(number), "error")
        return status
        #return_string = interface + ": " + status
        #return return_string

    def interface_utilization(self, interface, seconds=1):
        if_index = self.interface_select(interface)

        if if_index == 0:
            return "Interface not found"
        # problem z dlugim (10s) czasem wykonywania, ale mozna podzielić na dwa i odpalać na początku i koncu
        # a dokladna roznice czasu obliczac uzywajac uptime

        def run(direction):
            oid = " "
            if direction == "input":
                oid = '1.3.6.1.2.1.2.2.1.10.' + str(if_index)
            elif direction == "output":
                oid = '1.3.6.1.2.1.2.2.1.16.' + str(if_index)
            snmp_get = self.session.get(oid)

            start_time = time.time()

            if_in_octets_start = snmp_get.value

            time.sleep(seconds)

            stop_time = time.time()
            time_delta = stop_time - start_time
            snmp_get = self.session.get(oid)
            if_in_octets_stop = snmp_get.value
            delta_if_in_octets = int(if_in_octets_stop) - int(if_in_octets_start)

            oid = '1.3.6.1.2.1.2.2.1.5.' + str(if_index)

            snmp_get = self.session.get(oid)
            if_speed = snmp_get.value

            utilization = (delta_if_in_octets*8*100)/(time_delta*int(if_speed))
            # print(if_in_octets_start)
            # print(if_in_octets_stop)
            # print(delta_if_in_octets)
            return utilization

        input = round(run("input"), 2)
        output = round(run("output"), 2)
        #print(czas.datetime.now().time())
        result = "Input: " + str(input) + " Mbps, Output: " + str(output) + " Mbps."
        return result

    def interface(self, interface, what):
        int_status = []
        dictionary = {}
        interface_list = interface.split(",")
        if what == "status":
            for int in interface_list:
                int_status.append(self.interface_status(int))
                dictionary = dict(zip(interface_list, int_status))
            return dictionary
        if what == "utilization":
            for int in interface_list:
                int_status.append(self.interface_utilization(int))
                dictionary = dict(zip(interface_list, int_status))
            return dictionary

    def chassis_temperature(self):
        snmp_get = self.session.get('1.3.6.1.4.1.9.9.13.1.3.1.3.1')
        temperature = snmp_get.value + " °C"
        return temperature

    def fan_status(self):
        fans = []
        fans_status = []
        items = self.session.walk('1.3.6.1.4.1.9.9.13.1.4.1.2')
        for item in items:
            fans.append(item.value)
        items = self.session.walk('1.3.6.1.4.1.9.9.13.1.4.1.3')
        for item in items:
            if item.value == '1':
                fans_status.append("Normal")
            elif item.value == '2':
                fans_status.append("Warning")
            elif item.value == '3':
                fans_status.append("Critical")
            elif item.value == '4':
                fans_status.append("Shutdown")
            elif item.value == '5':
                fans_status.append("Not present")
            elif item.value == '6':
                fans_status.append("Not functioning")
        dictionary = dict(zip(fans, fans_status))
        return dictionary

# spr = Checker(['1', 'Router V1', 'Routers', 'Opis', '192.168.202.1', '2', 'Password', 'Admin', 'authPriv', 'MD5', 'Password',
#           'DES', 'Password', True, False, False, 'FastEthernet0/1,FastEthernet0/0', True, False])
# print(spr.interface('FastEthernet0/1', 'utilization'))
