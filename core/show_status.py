from core.database_engine import *
import json


class ShowStatus(DatabaseEngine):

    def get_host_id(self):
        session = scoped_session(session_factory)
        session = session()
        query = session.query(Host.id).filter_by(is_on=1)
        result = []
        for item in query:
            result.append(item[0])
        session.rollback()
        return result

    def append_service(self, service_name, service, type):  # bedzie zwracac to co potem trzeba services.append
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

    # def get_name(self, id):
    #     session = DatabaseEngine().connect()
    #     return session.query(Host.name).filter_by(id=id).first()[0]
    #
    # def get_address(self, id):
    #     session = DatabaseEngine().connect()
    #     return session.query(Host.address).filter_by(id=id).first()[0]
    #
    # def get_description(self, id):
    #     session = DatabaseEngine().connect()
    #     return session.query(Host.description).filter_by(id=id).first()[0]
    #
    # def get_date(self, id):
    #     session = DatabaseEngine().connect()
    #     return session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().date


    #
    # def get_uptime(self, id):
    #     session = DatabaseEngine().connect()
    #     uptime = session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().uptime
    #     if uptime:
    #         return self.append_service("Uptime", uptime, "list")
    #
    # def get_interface(self, id):
    #     session = DatabaseEngine().connect()
    #     interface = session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().interface
    #     if interface:
    #         return self.append_service("", interface, "dict")
    #
    # def get_chassis_temperature(self, id):
    #     session = DatabaseEngine().connect()
    #     chassis_temperature = session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().chassis_temperature
    #     if chassis_temperature:
    #         return self.append_service("Chassis Temp", chassis_temperature, "list")
    #
    # def get_fan_status(self, id):
    #     session = DatabaseEngine().connect()
    #     fan_status = session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().fan_status
    #     if fan_status:
    #         return self.append_service("", fan_status, "dict")
    #
    # def get_cpu_utilization(self, id):
    #     session = DatabaseEngine().connect()
    #     cpu_utilization = session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().cpu_utilization
    #     if cpu_utilization:
    #         return self.append_service("", cpu_utilization, "dict")


## ^^ w database engine


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

# database = [[[1, 'Admin', '192.168.202.254', 'Router in admin room', datetime.datetime(2017, 11, 13, 18, 44, 17, 96366), [['FastEthernet0/0', 'Input: 0.03 Mbps (0.0 %) Output 0.13 Mbps (0.0 %)', '0'], ['FastEthernet0/1', 'Down', '2'], ['Fan  1', 'Normal', '0'], ['Fan  2', 'Normal', '0'], ['RTT', '2.212', '1'], ['Uptime', '3:24:38', '0'], ['chassis_temperature', 'No such instance', '1']]], [2, 'Emplojes', '10.10.10.9', 'Router in employees room', datetime.datetime(2017, 11, 13, 18, 43, 48, 215819), [['FastEthernet0/0', 'Input: 56.95 Mbps (0.57 %) Output 0.02 Mbps (0.0 %)', '0'], ['FastEthernet0/1', 'Down', '2'], ['Serial0/2/0', 'Input: 0.0 Mbps (0.0 %) Output 0.0 Mbps (0.0 %)', '0'], ['Serial0/2/1', 'Input: 0.0 Mbps (0.0 %) Output 0.01 Mbps (0.0 %)', '0'], ['Fan  1', 'Normal', '0'], ['Fan  2', 'Normal', '0'], ['RTT', '229.407', '1'], ['Uptime', '1:54:50', '0'], ['chassis_temperature', 'No such instance', '1']]], [3, 'Core', '10.10.10.5', 'Core router (ISP)', datetime.datetime(2017, 11, 13, 18, 43, 48, 90100), [['Serial0/2/0', 'Input: 0.0 Mbps (0.0 %) Output 0.0 Mbps (0.0 %)', '0'], ['Serial0/2/1', 'Input: 0.51 Mbps (3.98 %) Output 0.59 Mbps (4.61 %)', '0'], ['Fan  1', 'Normal', '0'], ['Fan  2', 'Normal', '0'], ['RTT', '13.355', '1'], ['Uptime', '1:54:01', '0'], ['chassis_temperature', 'No such instance', '1']]]]]