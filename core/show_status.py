from core.database_engine import *
import ast
import json
import datetime
# def get_services_state():
#     one_host = []
#     database = []
#     host_and_services = session.query(Host).all()
#     for host in host_and_services:
#         host_id = host.id
#         one_host.append(host.name)
#         one_host.append(host.address)
#         one_host.append(host.description)
#         last_check = session.query(ServicesState).filter_by(host_id=host_id).order_by(
#             ServicesState.date.desc()).first().services_states
#         last_check_date = session.query(ServicesState).filter_by(host_id=host_id).order_by(
#             ServicesState.date.desc()).first().date
#         one_host.append(last_check_date)
#         one_host.append(last_check)
#         database.append(one_host)
#         one_host = []
#     return database


class ShowStatus():

    # def get_column(self, column):
    #     session = scoped_session(session_factory)
    #     session = session()
    #     query = session.query(column)
    #     result = []
    #     for item in query:
    #         result.append(item[0])
    #     return result

    def get_host_id(self):
        session = scoped_session(session_factory)
        session = session()
        query = session.query(Host.id).filter_by(is_on=1)
        result = []
        for item in query:
            result.append(item[0])
        return result

    def get_json(self, field):
        result = []
        if field is not "":
            temp = str(field).replace("'", '"')
            temp = json.loads(temp)
            for key in temp:
                result.append({key: temp[key]})
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


    def get_state(self, id, all=1):  # dla jednego!
        session = scoped_session(session_factory)
        session = session()

        result = []
        services = []

        name = session.query(Host.name).filter_by(id=id).first()
        address = session.query(Host.address).filter_by(id=id).first()
        description = session.query(Host.description).filter_by(id=id).first()

        if session.query(ServicesState).first() is None:
            return 0

        date = session.query(ServicesState).filter_by(host_id=id).order_by(
            ServicesState.date.desc()).first().date
        ping = session.query(ServicesState).filter_by(host_id=id).order_by(
            ServicesState.date.desc()).first().ping
        uptime = session.query(ServicesState).filter_by(host_id=id).order_by(
            ServicesState.date.desc()).first().uptime
        interface = session.query(ServicesState).filter_by(host_id=id).order_by(
            ServicesState.date.desc()).first().interface
        chassis_temperature = session.query(ServicesState).filter_by(host_id=id).order_by(
            ServicesState.date.desc()).first().chassis_temperature
        fan_status = session.query(ServicesState).filter_by(host_id=id).order_by(
            ServicesState.date.desc()).first().fan_status

        uptime = self.append_service("Uptime", uptime, "list")
        ping = self.append_service("RTT", ping, "list")
        chassis_temperature = self.append_service("chassis_temperature", chassis_temperature, "list")
        interface = self.append_service("", interface, "dict")
        fan_status = self.append_service("", fan_status, "dict")

        if interface:
            services.extend(interface)

        if fan_status:
            services.extend(fan_status)

        # if interface is not "":
        #     temp = str(interface).replace("'", '"')
        #     temp = json.loads(temp)
        #     print(temp)
        #     for key in sorted(temp):
        #         temp2 = temp[key].split("|")
        #         print(temp[key])
        #         services.append([key, temp2[0], temp2[1]])



        # if uptime is not "":
        #     # uptime = ["Uptime", uptime]
        #     service_name = ["Uptime"]
        #     data = uptime.split("|")
        #     uptime = service_name + data
        # if ping is not "":
        #     service_name = ["RTT"]
        #     data = ping.split("|")
        #     ping = service_name + data
        # if chassis_temperature is not "":
        #     chassis_temperature = ["chassis_temperature", chassis_temperature]
        # uptime = self.append_service("Uptime", uptime, "list")


        # metoda append_service w której bedzie się dodawac seriws
        # z w argumentami (service, type) gdzie type to bedzie czy lista
        # czy dict i w niej sprawdzanie usluga[2] czy jest tam wartosc 0 czy
        # może 1 oraz 2 co wskazuje na blad i zeby wyswietlic
        if ping and ping is not "":
            services.append((ping))

        if uptime and uptime is not "":
            services.append((uptime))

        if chassis_temperature and chassis_temperature is not "":
            services.append((chassis_temperature))
        #
        # if chassis_temperature is not "":
        #     services.append((chassis_temperature))
        #
        # if fan_status is not "":
        #     temp = str(fan_status).replace("'", '"')
        #     temp = json.loads(temp)
        #     for key in sorted(temp):
        #         services.append([key, temp[key]])


        #print(services)

        if all == 0:
            print(services)
            services = [item for item in services if item[2] != '0']

        result.extend((name[0], address[0], description[0], date))
        result.append(services)
        #print(result[4][1])
        return result

    def run(self, all):
        database = []
        host_id = self.get_host_id()
        for id in host_id:
            database.append(self.get_state(id, all))
        # database = [['Nazwa 1', '192.168.202.1', 'Opis 1', datetime.datetime(2017, 11, 9, 17, 20, 9, 132378), [['FastEthernet0/1', 'Input 0.0 % Output 0.0 %', '0'], ['FastEthernet0/2', 'Interface not found', '1'], ['Fan 1', 'Normal', '0'], ['Fan 2', 'Normal', '0'], ['Fan 3', 'Normal', '0'], ['RTT', '1.074', '0'], ['Uptime', '1:29:58', '0'], ['chassis_temperature', '20 °C', '0']]], ['nazwa 2 ', '192.168.202.1', 'Opis 2', datetime.datetime(2017, 11, 9, 17, 20, 9, 130616), [['Fan 1', 'Normal', '0'], ['Fan 2', 'Normal', '0'], ['Fan 3', 'Normal', '0'], ['RTT', '1.233', '1'], ['chassis_temperature', '20 °C', '0']]], ['Widmo', '192.168.202.69', 'Opis ma byc I ten host ma nie dzialac.', datetime.datetime(2017, 11, 9, 17, 20, 8, 969339), [['RTT', 'Destination Host Unreachable', '2']]]]
        return database

    # def get_states(self):
    #     session = scoped_session(session_factory)
    #     session = session()
    #     services = []
    #     host_data = []
    #     host_data_raw = []
    #     last_check_date = []
    #     host_id = self.get_host_id()
    #     name = self.get_column(Host.name)
    #     address = self.get_column(Host.address)
    #     description = self.get_column(Host.description)
    #
    #     for id in host_id:
    #         date = session.query(ServicesState).filter_by(host_id=id).order_by(
    #             ServicesState.date.desc()).first().date
    #         last_check_date.append(date)
    #     #print(name)
    #     #print(last_check_date)
    #     host_data_raw.extend((host_id, name, address, description, last_check_date))
    #     temp = list(zip(*host_data_raw))
    #     for item in temp:
    #         host_data.append(list(item))
    #
    #     for id in host_data_raw[0]:
    #         temp_2 = []
    #         ping = session.query(ServicesState).filter_by(host_id=id).order_by(
    #             ServicesState.date.desc()).first().ping
    #         uptime = session.query(ServicesState).filter_by(host_id=id).order_by(
    #             ServicesState.date.desc()).first().uptime
    #         interface = session.query(ServicesState).filter_by(host_id=id).order_by(
    #             ServicesState.date.desc()).first().interface
    #         chassis_temperature = session.query(ServicesState).filter_by(host_id=id).order_by(
    #             ServicesState.date.desc()).first().chassis_temperature
    #         fan_status = session.query(ServicesState).filter_by(host_id=id).order_by(
    #             ServicesState.date.desc()).first().fan_status
    #
    #
    #         #temp_json = interface.replace("'", '"')
    #         #print(repr(temp_json))
    #
    #
    #         temp_2.extend((uptime.split("|"), ping.split("|"), interface,
    #                        chassis_temperature.split("|"), fan_status))
    #         services.append(temp_2)
    #         #print(temp_2)
    #
    #
    #
    #
    #         #print(n["attr1"])
    #         #print(n["attr1"])
    #         #chyba_json = json.dumps(chyba_json)
    #         #d = json.loads(chyba_json)
    #         #print(d['key1'])
    #
    #     i = 0
    #     for item in services:
    #         host_data[i].append(item)
    #         i += 1
    #
    #     #print(host_data)
    #     return host_data

# all_states = ShowStatus()
# database = all_states.get_states()
# print(database)



# host_id = test.get_column(Host.id)
# print(host_id)
#
#
#

#
# print(result)



# robimy klase z tej funkcji i metody get_name get address itp

# services = session.query(ServicesState).filter_by(host_id=2).all()
# print(services)
#
# last_check = session.query(ServicesState).filter_by(host_id=2).order_by(ServicesState.date.desc()).first().services_states
# #print(last_check)

