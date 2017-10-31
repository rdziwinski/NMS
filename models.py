
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:////root/home/user/NMS/data/database.db', echo=True)


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

    services_states = relationship('ServicesState', back_populates="host")

    def __repr__(self):
        return "<User(name='%s', category='%s', description='%s')>" % (
            self.name, self.category, self.description)


class ServicesState(Base):
    __tablename__ = 'services_state'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(30))
    uptime = Column(Boolean)
    ping = Column(Boolean)
    interface_status = Column(String(30))
    interface_utilization = Column(String(30))
    chassis_temperature = Column(Boolean)
    fan_status = Column(Boolean)

    host_id = Column(Integer, ForeignKey('hosts.id'))
    host = relationship("Host", back_populates="services_states")
