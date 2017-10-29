from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '123456790'


class Host(db.Model):
    #id = db.Column(db.Integer, db.ForeignKey('Service.id'),
    #               primary_key=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    category = db.Column(db.String(30))
    description = db.Column(db.String(255))
    address = db.Column(db.String(40))
    snmp_version = db.Column(db.String(2))
    community = db.Column(db.String(30))
    security_name = db.Column(db.String(30))
    security_level = db.Column(db.String(30))
    auth_protocol = db.Column(db.String(30))
    priv_key = db.Column(db.String(30))
    priv_protocol = db.Column(db.String(30))
    auth_key = db.Column(db.String(30))
    uptime = db.Column(db.Boolean)
    ping = db.Column(db.Boolean)
    interface_status = db.Column(db.String(30))
    interface_utilization = db.Column(db.String(30))
    chassis_temperature = db.Column(db.Boolean)
    fan_status = db.Column(db.Boolean)

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

        #service_state = db.relationship('Service', backref=db.backref('hosts', lazy=True))

    def __repr__(self):
        return self.name

    def add(self, data, category, erase):  # dodac obsluge bledu jak juz jest host dodany UNIQUE
        #try:
        db.session.rollback()
        if erase == ['erase']:
            db.drop_all()
        db.create_all()
        for i in range(1, len(data[1])):
            host = Host(data[0][i], category, data[1][i], data[2][i], data[3][i], data[4][i], data[5][i], data[6][i],
                        data[7][i], data[8][i], data[9][i], data[10][i], data[11][i], data[12][i],
                        data[13][i], data[14][i], data[15][i])
            db.session.add(host)
        db.session.commit()
       # except:
        #    return 1

    def show_all(self):
        one_host = []
        database = []
        hosts = self.query.all()
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


# class Service(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     uptime = db.Column(db.Boolean)
#     ping = db.Column(db.Boolean)
#     interface_status = db.Column(db.String(30))
#     interface_utilization = db.Column(db.String(30))
#     chassis_temperature = db.Column(db.Boolean)
#     fan_status = db.Column(db.Boolean)
