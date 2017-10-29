import datetime
from multiprocessing.dummy import Pool as ThreadPool
from core.checker import *



hosts = [['1', 'Router V1', 'Routers', 'Opis', '192.168.202.1', '2', 'Password', 'Admin', 'authPriv', 'MD5', 'Password',
          'DES', 'Password', True, False, False, 'FastEthernet0/1,FastEthernet0/0', True, False],
         ['2', 'Router V2', 'Routers', 'Opis asdasd', '192.168.202.1', '2', 'Password', 'Admin', 'authPriv', 'MD5',
          'Password', 'DES', 'Password', True, False, False, 'FastEthernet0/1,FastEthernet0/0', True, True]]


class CheckEngine:
    def check_service(self, host):
        result = []

        spr = Checker(host)
        if host[13] is True:
            result.append(spr.uptime())
        if host[14] is True:
            result.append("ping")
        if host[15] is not False and host[15] is not None:
            result.append(spr.interface(host[15], 'status'))
        if host[16] is not False and host[15] is not None:
            result.append(spr.interface(host[16], 'utilization'))
        if host[17] is True:
            result.append(spr.chassis_temperature())
        if host[18] is True:
            result.append(spr.fan_status())
        return result

    def run(self, host):
        result = []
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        result.append(str(date).split(".")[0])
        result.append(str(time).split(".")[0])
        result.append(self.check_service(host))
        return result
