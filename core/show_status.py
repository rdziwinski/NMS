from core.database_engine import *

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
    def get_column(self, column):
        query = session.query(column)
        result = []
        for item in query:
            result.append(item[0])
        return result

    def get_last_checks(self, id):
        #last_check = session.query(ServicesState).filter_by(host_id=1).order_by(ServicesState.date.desc()).first().services_states
        last_check_date = session.query(ServicesState).filter_by(host_id=id).order_by(ServicesState.date.desc()).first().date
        return last_check_date

    def get_states(self):

        services = []
        host_data = []
        host_data_raw = []
        host_id = self.get_column(Host.id)
        name = self.get_column(Host.name)
        address = self.get_column(Host.address)
        description = self.get_column(Host.description)

        host_data_raw.extend((host_id, name, address, description))
        temp = list(zip(*host_data_raw))
        for item in temp:
            host_data.append(list(item))

        for id in host_data_raw[0]:
            temp_2 = []
            uptime = session.query(ServicesState).filter_by(host_id=id).order_by(
                ServicesState.date.desc()).first().uptime
            ping = session.query(ServicesState).filter_by(host_id=id).order_by(
                ServicesState.date.desc()).first().ping
            interface_status = session.query(ServicesState).filter_by(host_id=id).order_by(
                ServicesState.date.desc()).first().interface_status
            interface_utilization = session.query(ServicesState).filter_by(host_id=id).order_by(
                ServicesState.date.desc()).first().interface_utilization
            chassis_temperature = session.query(ServicesState).filter_by(host_id=id).order_by(
                ServicesState.date.desc()).first().chassis_temperature
            fan_status = session.query(ServicesState).filter_by(host_id=id).order_by(
                ServicesState.date.desc()).first().fan_status
            temp_2.extend((uptime, ping, interface_status, interface_utilization, chassis_temperature, fan_status))
            services.append(temp_2)

        i = 0
        for item in services:
            host_data[i].append(item)
            i += 1
        return host_data

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

