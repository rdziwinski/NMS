# Router interface: 192.168.202.1
# Windows interface: 192.168.202.1
# Linux interface: 192.168.202.3
# Project files: /home/user/checker
from easysnmp import Session
from datetime import timedelta
import ast
import os
import time
import subprocess
import datetime as czas
import json

class Checker():
    def __init__(self, host):
        self.ip_address = host[4]
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
        uptime = str(date).split(".")[0]
        # result = {"Uptime": uptime}
        return uptime

    def ping(self):
        data = os.popen("ping " + self.ip_address + " -c 1").read()
        time.sleep(0.1)
        data = str(data)
        if "ttl" in data:
            rtt = data.split("/")[-3]
            # result = {"RTT": rtt}
            return rtt
        elif "Destination Host Unreachable" in data:
            unreachable = "Destination Host Unreachable"
            return unreachable
        else:
            not_know = "Name or service not known"
            return not_know

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
        else:
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
        result = "Input " + str(input) + " Mbps. Output " + str(output) + " Mbps."
        return result

    def interface(self, interfaces):
        interfaces_results = []
        result = []
        interface_list = interfaces.split(",")
        for int in interface_list:
            int_status = self.interface_status(int)
            if int_status is not "Down":
                int_utilization = self.interface_utilization(int)
                interfaces_results.append(int_utilization)
            else:
                interfaces_results.append(int_status)
        aaa = dict(zip(interface_list, interfaces_results))
        print(aaa)
        return aaa



        # interfaces_status = []
        # dictionary = {}
        # interface_list = interfaces.split(",")
        # for int in interface_list:
        #     #print(int)
        #     int_status = self.interface_status(int)
        #    # if int_status is not "Up":
        #        # print(int)
        #        # print("duuuupa")
        #
        #     #interfaces_status.append()
        #     #interfaces_status.append(self.interface_utilization(int))
        #     #dictionary = dict(zip(interface_list, interfaces_status))
        # return "cycki"

    def chassis_temperature(self):
        snmp_get = self.session.get('1.3.6.1.4.1.9.9.13.1.3.1.3.1')
        temperature = snmp_get.value + " °C"
        # result = {"Chassis  temperatur": temperature}
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
