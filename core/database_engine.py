from core.models import *
from sqlalchemy import desc


class DatabaseEngine():
    def __init__(self):
        session = scoped_session(session_factory)
        self.session = session()

    def connect(self):
        session = scoped_session(session_factory)
        return session()

    def get_name(self, id):
        return self.session.query(Host.name).filter_by(id=id).first()[0]

    def get_address(self, id):
        return self.session.query(Host.address).filter_by(id=id).first()[0]

    def get_description(self, id):
        return self.session.query(Host.description).filter_by(id=id).first()[0]

    def get_date(self, id):
        return self.session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().date

    def get_ping(self, id):
        return self.session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().ping

    def get_uptime(self, id):
        return self.session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().uptime

    def get_interface(self, id):
        return self.session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().interface

    def get_chassis_temperature(self, id):
        return self.session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().chassis_temperature

    def get_fan_status(self, id):
        return self.session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().fan_status

    def get_cpu_utilization(self, id):
        return self.session.query(Check).filter_by(host_id=id).order_by(Check.date.desc()).first().cpu_utilization





    def add_host(self, data, category, erase):  # dodac obsluge bledu jak juz jest host dodany UNIQUE
        session = scoped_session(session_factory)
        session = session()
        session.rollback()
        if erase == ['erase']:
            Base.metadata.drop_all(engine)  # Host.__table__.drop(engine)
        Base.metadata.create_all(engine)
        for i in range(1, len(data[1])):
            host = Host(data[0][i], category, data[1][i], data[2][i], data[3][i], data[4][i], data[5][i], data[6][i],
                        data[7][i], data[8][i], data[9][i], data[10][i], data[11][i], data[12][i],
                        data[13][i], data[14][i], data[15][i], data[16][i])
            session.add(host)
            session.commit()
            session.rollback()

    def get_hosts(self, all=1, id=0):
        one_host = []
        database = []
        hosts = []
        session = scoped_session(session_factory)
        session = session()
        if all == 1:
            hosts = session.query(Host).all()
        elif all == 0:
            hosts = session.query(Host).filter_by(id=id).first()
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
            one_host.append(host.interface)
            one_host.append(host.uptime)
            one_host.append(host.chassis_temperature)
            one_host.append(host.fan_status)
            one_host.append(host.cpu_utilization)
            one_host.append(host.is_on)
            database.append(one_host)
            one_host = []
        return database

    def get_checks(self):
        one_check = []
        database = []
        session = scoped_session(session_factory)
        session = session()
        host_and_services = session.query(Check).order_by(desc(Check.id)).all()
        for check in host_and_services:
            one_check.append(check.id)
            one_check.append(check.host_id)
            one_check.append(check.date)
            one_check.append(check.ping)
            one_check.append(check.interface)
            one_check.append(check.uptime)
            one_check.append(check.chassis_temperature)
            one_check.append(check.fan_status)
            one_check.append(check.cpu_utilization)
            database.append(one_check)
            one_check = []
        return database
