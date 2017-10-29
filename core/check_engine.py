from core.checker import Checker
import datetime
import time as timee


class CheckEngine(Checker):
    def __init__(self, hosts):
        self.hosts = hosts

    def run(self, check):




hosts = [['Router V1', 'Routers', 'Opis', '192.168.1.1', '3', None, 'Admin', 'authPriv', 'MD5', 'Password',
          'DES', 'Password', True, False, 'interface_status', 'interface_utilization', True, False],
         ['Router V2', 'Routers', 'Opis asdasd', '192.168.1.2', '3', None, 'Admin', 'authPriv', 'MD5',
          'Password', 'DES', 'Password', True, True, 'fa0/1', 'fa0/1', None, False],
         ['Switch drugi', 'Switches', 'Opis 2', '192.168.1.5', '3', None, 'Admin', 'authPriv', 'MD5',
          'Password', 'DES', 'ok', True, True, 'fa0/3', 'fa0/3', True, False],
         ['Switch glowny4', 'Switches', 'Opisdwa', '192.168.1.6', '2c', 'Password', None, None, None, None, None,
          None, True, True, 'fa0/3', 'fa0/3', True, False]]

check = Checker()


def test(ipaddress):
    timee.sleep(1)
    temp = "test: " + ipaddress
    return temp


result = []
for i in range(0, len(hosts)):
    temp = []
    if hosts[i][13] is True:
        temp2 = []
        time = datetime.datetime.now().time()
        temp2.append(str(time).split(".")[0])
        temp2.append("Ping")
        temp2.append(check.ping(hosts[i][3]))
        temp.append(temp2)
    if hosts[i][12] is True:
        temp2 = []
        time = datetime.datetime.now().time()
        temp2.append(str(time).split(".")[0])
        temp2.append("Test")
        temp2.append(test(hosts[i][1]))
        temp.append(temp2)
    result.append(temp)


print(result)

# name	description	address	snmp_version	community	security_name	security_level	auth_protocol	priv_key	priv_protocol	auth_key	uptime	ping	interface_status	interface_utilization	chassis_temperature	fan_status
