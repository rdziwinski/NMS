from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
Base = declarative_base()
engine = create_engine('sqlite:////root/home/user/NMS/data/database.db', echo=False,
                       connect_args={'check_same_thread': False})

# engine = create_engine('sqlite:///C:/Users/rdziw/Documents/Python/NMS/data/database_2.db', echo=True,
#                        connect_args={'check_same_thread': False})

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
    uptime = Column(String(30))
    interface = Column(String(30))
    chassis_temperature = Column(Boolean)
    fan_status = Column(Boolean)
    is_on = Column(Boolean)

    def __repr__(self):
        return "<User(name='%s', category='%s', description='%s')>" % (
            self.name, self.category, self.description)

    def __init__(self, name="",  category="", description="", address="", snmp_version="", community="", security_name="",
                 security_level="", auth_protocol="", priv_key="", priv_protocol="", auth_key="",
                 uptime="", interface="", chassis_temperature="",
                 fan_status="", is_on=""):
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
        self.interface = interface
        self.chassis_temperature = chassis_temperature
        self.fan_status = fan_status
        self.is_on = is_on


class ServicesState(Base):
    __tablename__ = 'services_state'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer)
    date = Column(DateTime)  # tu ma byc datetime
    uptime = Column(String(30))
    ping = Column(String(30))
    interface = Column(String(30))
    chassis_temperature = Column(String(30))
    fan_status = Column(String(128))

    def __init__(self, host_id="", date="", ping="", uptime="", interface="", chassis_temperature="", fan_status=""):
        self.host_id = host_id
        self.date = date
        self.ping = ping
        self.uptime = uptime
        self.interface = interface
        self.chassis_temperature = chassis_temperature
        self.fan_status = fan_status
