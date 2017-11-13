from core.models import *
from sqlalchemy import desc
class Database(Host, ServicesState):
    def add_host(self, data, category, erase):  # dodac obsluge bledu jak juz jest host dodany UNIQUE
        session = scoped_session(session_factory)
        session = session()
        session.rollback()
        if erase == ['erase']:
            #print("tu bylo usuwanie")
            Base.metadata.drop_all(engine)
            #Host.__table__.drop(engine)
        Base.metadata.create_all(engine)
        for i in range(1, len(data[1])):
            host = Host(data[0][i], category, data[1][i], data[2][i], data[3][i], data[4][i], data[5][i], data[6][i],
                        data[7][i], data[8][i], data[9][i], data[10][i], data[11][i], data[12][i],
                        data[13][i], data[14][i], data[15][i])
            session.add(host)
            session.commit()
            session.rollback()
            #print(data)
            # except:
            #    return 1

    def get_hosts(self):
        # session.rollback()
        one_host = []
        database = []
        session = scoped_session(session_factory)
        session = session()
        hosts = session.query(Host).all()
        for host in hosts:
            one_host.append(host.id)
            one_host.append(host.name)
            one_host.append(host.category)
            one_host.append(host.description)
            one_host.append(host.address)
            one_host.append(host.snmp_version)
            one_host.append(host.community)
            one_host.append(host.security_name)
            one_host.append(host.security_level)
            one_host.append(host.auth_protocol)
            one_host.append(host.priv_key)
            one_host.append(host.priv_protocol)
            one_host.append(host.auth_key)
            one_host.append(host.uptime)
            one_host.append(host.interface)
            one_host.append(host.chassis_temperature)
            one_host.append(host.fan_status)
            one_host.append(host.is_on)
            database.append(one_host)
            one_host = []
        return database

    def get_services_states(self):
        session = scoped_session(session_factory)
        session = session()
        services = session.query(ServicesState).all()
        #print(services)
        return services

    # def add_services_state(self, data):
    #     session.rollback()
    #     Base.metadata.create_all(engine)
    #     services_state = ServicesState()
    #     session.add(services_state)
    #     session.commit()

    def show_services(self):
        one_check = []
        database = []
        session = scoped_session(session_factory)
        session = session()
        host_and_services = session.query(ServicesState).order_by(desc(ServicesState.id)).all()
        for check in host_and_services:
            one_check.append(check.id)
            one_check.append(check.host_id)
            one_check.append(check.date)
            one_check.append(check.ping)
            one_check.append(check.uptime)
            one_check.append(check.interface)
            one_check.append(check.chassis_temperature)
            one_check.append(check.fan_status)
            database.append(one_check)
            one_check = []
        return database
