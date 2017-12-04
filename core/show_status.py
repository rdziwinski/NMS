from core.database_engine import *
import json


class ShowStatus(DatabaseEngine):
    def append_service(self, service_name, service, type):
        if service is not "":
            if type == 'list':
                data = service.split("|")
                result = [service_name] + data
                return result
            elif type == 'dict':
                result = []
                temp = str(service).replace("'", '"')
                temp = json.loads(temp)
                for key in sorted(temp):
                    temp2 = temp[key].split("|")
                    result.append([key, temp2[0], temp2[1]])
                return result

    def get_host_data(self, id):
        host_data = []
        host_data.extend((id, self.get_name(id), self.get_address(id), self.get_description(id), self.get_date(id)))
        return host_data

    def get_host_services(self, id, all):
        session = scoped_session(session_factory)
        session = session()
        services = []

        if session.query(Check).first() is None:
            return 0

        uptime = self.get_uptime(id)
        ping = self.get_ping(id)
        chassis_temperature = self.get_chassis_temperature(id)
        interface = self.get_interface(id)
        fan_status = self.get_fan_status(id)
        cpu_utilization = self.get_cpu_utilization(id)

        if ping:
            services.append(self.append_service("RTT", ping, "list"))
        if interface:
            services.extend(self.append_service("", interface, "dict"))
        if fan_status:
            services.extend(self.append_service("", fan_status, "dict"))
        if cpu_utilization:
            services.extend(self.append_service("", cpu_utilization, "dict"))
        if uptime:
            services.append(self.append_service("Uptime", uptime, "list"))
        if chassis_temperature:
            services.append(self.append_service("Chassis Temp", chassis_temperature, "list"))
        if all == 0:
            services = [item for item in services if item[2] != '0']
        return services

    def run(self, all):
        database = []
        host_id = self.get_host_id()
        for id in host_id:
            temp = []
            temp.extend(self.get_host_data(id))
            temp.append(self.get_host_services(id, all))
            database.append(temp)
        return database
