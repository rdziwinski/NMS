from core.database_engine import *


def get_services_state():
    one_host = []
    database = []
    host_and_services = session.query(Host).all()
    for host in host_and_services:
        host_id = host.id
        one_host.append(host.name)
        one_host.append(host.address)
        one_host.append(host.description)
        last_check = session.query(ServicesState).filter_by(host_id=host_id).order_by(
            ServicesState.date.desc()).first().services_states
        last_check_date = session.query(ServicesState).filter_by(host_id=host_id).order_by(
            ServicesState.date.desc()).first().date
        one_host.append(last_check_date)
        one_host.append(last_check)
        database.append(one_host)
        one_host = []
    return database


# robimy klase z tej funkcji i metody get_name get address itp



# services = session.query(ServicesState).filter_by(host_id=2).all()
# print(services)
#
# last_check = session.query(ServicesState).filter_by(host_id=2).order_by(ServicesState.date.desc()).first().services_states
# #print(last_check)



print(get_services_state())