from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '123456790'


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
