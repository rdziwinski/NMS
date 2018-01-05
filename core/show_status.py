from core.database_engine import *
import json


class ShowStatus(DatabaseEngine):
    def append_parameter(self, status_data, type, parameter_name=""):
        if status_data is not "":
            if type == 'list':
                data = status_data.split("|")
                result = [parameter_name] + data
                return result
            elif type == 'dict':
                result = []
                temp = str(status_data).replace("'", '"')
                temp = json.loads(temp)
                for key in sorted(temp):
                    temp2 = temp[key].split("|")
                    result.append([key, temp2[0], temp2[1]])
                return result

    def get_host_data(self, id):
        host_data = []
        host_data.extend((id, self.get_name(id), self.get_address(id), self.get_description(id), self.get_date(id)))
        return host_data

    def get_host_parameters(self, id, problems):
        parameters = []

        uptime = self.get_uptime(id)
        ping = self.get_ping(id)
        chassis_temperature = self.get_chassis_temperature(id)
        interface = self.get_interface(id)
        fan_status = self.get_fan_status(id)
        cpu_utilization = self.get_cpu_utilization(id)

        if ping:
            parameters.append(self.append_parameter(ping, "list", "RTT"))
        if interface:
            parameters.extend(self.append_parameter(interface, "dict"))
        if fan_status:
            parameters.extend(self.append_parameter(fan_status, "dict"))
        if cpu_utilization:
            parameters.extend(self.append_parameter(cpu_utilization, "dict"))
        if uptime:
            parameters.append(self.append_parameter(uptime, "list", "Uptime"))
        if chassis_temperature:
            parameters.append(self.append_parameter(chassis_temperature, "list", "Chassis Temp"))
        if problems == 1:
            parameters = [item for item in parameters if item[2] != '0']
        return parameters

    def run(self, all):
        database = []
        hosts_id = self.get_hosts_id()
        for id in hosts_id:
            temp = []
            temp.extend(self.get_host_data(id))
            temp.append(self.get_host_parameters(id, all))
            database.append(temp)
        return database
