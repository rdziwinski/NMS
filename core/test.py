import json

data = {'interface': {'name': 'interface', 'critical': '40', 'warning': '40'}, 'chassis_temperature': {'name': 'Chassis temperature', 'critical': '10', 'warning': '5'}, 'fan_status': {'name': 'Fan status', 'critical': '10', 'warning': '5'}, 'ping': {'name': 'ping', 'critical': '10', 'warning': '5'}, 'uptime': {'name': 'Uptime', 'critical': '10', 'warning': '20'}}

path = os.path.dirname(os.path.abspath(__file__)) + "/data/services.json"

with open(path, 'w') as f:
    json.dump(data, f)
