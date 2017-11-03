import datetime
from multiprocessing.dummy import Pool as ThreadPool
from core.checker import *
from core.database_engine import *


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
        else:
            result.append("")
        if host[14] is True:
            result.append("ping")
        else:
            result.append("")
        if host[15] is not False and host[15] is not None:
            result.append(spr.interface(host[15], 'status'))
        else:
            result.append("")
        if host[16] is not False and host[15] is not None:
            result.append(spr.interface(host[16], 'utilization'))
        else:
            result.append("")
        if host[17] is True:
            result.append(spr.chassis_temperature())
        else:
            result.append("")
        if host[18] is True:
            result.append(spr.fan_status())
        else:
            result.append("")
        return result

    def run(self, host):
        result = []
        host_id = host[0]
        date = datetime.datetime.now()
        services_states = self.check_service(host)
        result.append(host_id)
        result.append(date)
        result.append(services_states)
        print("RESULT:")
        print(result)
        add_to_database = ServicesState(host_id=host_id, date=date, services_states=str(services_states))
        #print(add_to_database.host_id)
        #print(add_to_database.date)
        #print(add_to_database.services_states)

        session.rollback()
        session.add(add_to_database)
        session.commit()
        return result
