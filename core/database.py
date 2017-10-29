from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '123456790'


class Host(db.Model):
    name = db.Column(db.String(30), primary_key=True)  # Deklaracje pol bazy
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
    category = db.Column(db.String(30))

    def __init__(self, name="", description="", address="", snmp_version="", community="", security_name="",
                 security_level="", auth_protocol="", priv_key="", priv_protocol="", auth_key="", category=""):
        self.name = name
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
        self.category = category

    def __repr__(self):
        return self.name

    def add(self, data, category, erase): # dodac obsluge bledu jak juz jest host dodany UNIQUE
        #try:
        db.session.rollback()
        if erase == ['erase']:
            db.drop_all()
        db.create_all()
        for i in range(1, len(data[1])):
            host = Host(data[0][i], data[1][i], data[2][i], data[3][i], data[4][i], data[5][i], data[6][i],
                        data[7][i], data[8][i], data[9][i], data[10][i], category)
            db.session.add(host)
        db.session.commit()
       # except:
        #    return 1

    def show_all(self):
        one_host = []
        database = []
        hosts = self.query.all()
        for host in hosts:
            one_host.append(host.name)
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
            one_host.append(host.category)
            database.append(one_host)
            one_host = []
        return database

class Services(db.Model):
    category = db.Column(db.String(30), primary_key=True)
    uptime = db.Column(db.Boolean)  # Deklaracje pol bazy
    ping = db.Column(db.Boolean)
    interface_status = db.Column(db.String(30))
    interface_utilization = db.Column(db.String(30))
    chassis_temperature = db.Column(db.Boolean)
    fan_status = db.Column(db.Boolean)

    def __init__(self, category="", uptime="", ping="", interface_status="", interface_utilization="",
                 chassis_temperature="", fan_status=""):
        self.category = category
        self.uptime = uptime
        self.ping = ping
        self.interface_status = interface_status
        self.interface_utilization = interface_utilization
        self.chassis_temperature = chassis_temperature
        self.fan_status = fan_status

    def __repr__(self):
        return self.name

    def add(self, data):
        try:
            db.drop_all()
            db.create_all()
            for i in range(1, len(data[1])):
                services = Services(data[0][i], data[1][i], data[2][i], data[3][i], data[4][i], data[5][i], data[6][i])
                db.session.add(services)
            db.session.commit()
        except:
            return 1

    def show_category(self):
        one_category = []
        database = []
        category = self.query.all()
        for host in category:
            one_category.append(host.category)
            one_category.append(host.uptime)
            one_category.append(host.ping)
            one_category.append(host.interface_status)
            one_category.append(host.interface_utilization)
            one_category.append(host.chassis_temperature)
            one_category.append(host.fan_status)
            database.append(one_category)
            one_category = []
        return database