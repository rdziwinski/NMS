from core.database_engine import *
import ast
import json

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

    def get_state(self, id):  # dla jednego!
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

        if uptime is not "":
            # uptime = ["Uptime", uptime]
            service_name = ["Uptime"]
            data = uptime.split("|")
            uptime = service_name + data
        if ping is not "":
            service_name = ["RTT"]
            data = ping.split("|")
            ping = service_name + data
        if chassis_temperature is not "":
            chassis_temperature = ["chassis_temperature", chassis_temperature]

        if ping is not "":
            services.append((ping))

        if uptime is not "":
            services.append((uptime))

        if interface is not "":
            temp = str(interface).replace("'", '"')
            temp = json.loads(temp)
            for key in sorted(temp):
                temp2 = temp[key].split("|")
                print(temp2)
                services.append([key, temp2[0], temp2[1]])
                #services.append([key, temp[key].split("|")])

        if chassis_temperature is not "":
            services.append((chassis_temperature))

        if fan_status is not "":
            temp = str(fan_status).replace("'", '"')
            temp = json.loads(temp)
            for key in sorted(temp):
                services.append([key, temp[key]])


        #print(services)

        result.extend((name[0], address[0], description[0], date))
        result.append(services)
        #print(result[4][1])
        return result

    def run(self):
        database = []
        host_id = self.get_host_id()
        for id in host_id:
            database.append(self.get_state(id))
        #print(database)
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

