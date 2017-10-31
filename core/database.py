from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:////root/home/user/NMS/data/database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Host(Base):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    category = Column(String(30))
    description = Column(String(255))
    address = Column(String(40))
    snmp_version = Column(String(2))
    community = Column(String(30))
    security_name = Column(String(30))
    security_level = Column(String(30))
    auth_protocol = Column(String(30))
    priv_key = Column(String(30))
    priv_protocol = Column(String(30))
    auth_key = Column(String(30))
    uptime = Column(Boolean)
    ping = Column(Boolean)
    interface_status = Column(String(30))
    interface_utilization = Column(String(30))
    chassis_temperature = Column(Boolean)
    fan_status = Column(Boolean)

    #services_states = relationship('ServicesState')

    def __repr__(self):
        return "<User(name='%s', category='%s', description='%s')>" % (
            self.name, self.category, self.description)

    def __init__(self, name="",  category="", description="", address="", snmp_version="", community="", security_name="",
                 security_level="", auth_protocol="", priv_key="", priv_protocol="", auth_key="",
                 uptime="", ping="", interface_status="", interface_utilization="", chassis_temperature="",
                 fan_status=""):
        self.name = name
        self.category = category
        self.description = description
        self.address = address
        self.snmp_version = snmp_version
        self.community = community
        self.security_name = security_name
        self.security_level = security_level
        self.auth_protocol = auth_protocol
        self.priv_key = priv_key
        self.priv_protocol = priv_protocol
        self.auth_key = auth_key
        self.uptime = uptime
        self.ping = ping
        self.interface_status = interface_status
        self.interface_utilization = interface_utilization
        self.chassis_temperature = chassis_temperature
        self.fan_status = fan_status



    def add(self, data, category, erase):  # dodac obsluge bledu jak juz jest host dodany UNIQUE
        #try:
        session.rollback()
        if erase == ['erase']:
            Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        for i in range(1, len(data[1])):
            host = Host(data[0][i], category, data[1][i], data[2][i], data[3][i], data[4][i], data[5][i], data[6][i],
                        data[7][i], data[8][i], data[9][i], data[10][i], data[11][i], data[12][i],
                        data[13][i], data[14][i], data[15][i])
            session.add(host)
            session.commit()
       # except:
        #    return 1

    def get_hosts(self):
        one_host = []
        database = []
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
            one_host.append(host.ping)
            one_host.append(host.interface_status)
            one_host.append(host.interface_utilization)
            one_host.append(host.chassis_temperature)
            one_host.append(host.fan_status)
            database.append(one_host)
            one_host = []
        return database


class ServicesState(Base):
    __tablename__ = 'services_state'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer)
    date = Column(String(30))
    uptime = Column(Boolean)
    ping = Column(Boolean)
    interface_status = Column(String(30))
    interface_utilization = Column(String(30))
    chassis_temperature = Column(Boolean)
    fan_status = Column(Boolean)

    #host_id = Column(Integer, ForeignKey('Host.id'))
    #host = relationship("Host", back_populates="services_states")
