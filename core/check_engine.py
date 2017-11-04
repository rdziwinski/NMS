import datetime
from multiprocessing.dummy import Pool as ThreadPool
from core.checker import *
from core.database_engine import *

hosts = [['1', 'Router V1', 'Routers', 'Opis', '192.168.202.1', '2', 'Password', 'Admin', 'authPriv', 'MD5', 'Password',
          'DES', 'Password', True, False, False, 'FastEthernet0/1,FastEthernet0/0', True, False],
         ['2', 'Router V2', 'Routers', 'Opis asdasd', '192.168.202.1', '2', 'Password', 'Admin', 'authPriv', 'MD5',
          'Password', 'DES', 'Password', True, False, False, 'FastEthernet0/1,FastEthernet0/0', True, True]]


class CheckEngine:
    def run(self, host):
        if host[17] is True:
            check = Checker(host)
            host_id = host[0]
            date = datetime.datetime.now()
            ping_result = check.ping()
            if any(str.isdigit(c) for c in ping_result):
                self.check_snmp(host)
            else:
                add_to_database = ServicesState(host_id=host_id, date=date, ping=ping_result)
                session.add(add_to_database)
                session.commit()

    def check_snmp(self, host):
        # session.rollback()
        services_state = []
        check = Checker(host)
        host_id = host[0]
        date = datetime.datetime.now()
        # # print(type(date))
        # print("===:")
        # print(host)
        # print("===")
        services_state.append(check.ping())
        if host[13] is True or host[13] is '1':
            services_state.append(check.uptime())  # tymczasowe
        else:
            services_state.append("")  # towniez tymczasowe
        if host[14] is not False or host[14] is not '0':
            services_state.append(check.interface(host[14], 'status'))
        else:
            services_state.append("")
        if host[15] is True or host[15] is '1':
            services_state.append(check.chassis_temperature())
        else:
            services_state.append("")
        if host[16] is True or host[16] is '1':
            services_state.append(check.fan_status())
        else:
            services_state.append("")
        print("====")
        print(services_state)
        add_to_database = ServicesState(host_id=host_id, date=date, ping=services_state[0],
                                        uptime=str(services_state[1]), interface=str(services_state[2]),
                                        chassis_temperature=services_state[3], fan_status=str(services_state[4]))

        session.add(add_to_database)
        session.commit()




        # add_to_database = ServicesState(host_id=host_id, date=date, services_states=str(services_states))
        # print(add_to_database.host_id)
        # print(add_to_database.date)
        # print(add_to_database.services_states)

# hosty = [1, 'Router V1', 'Routers', 'Opis', '192.168.202.1', '2', 'Password', None, None, None, None, None, None, False,
#          False, 'FastEthernet0/0', False, True, True]
#
#
# test = CheckEngine()
# test.run(hosty)
