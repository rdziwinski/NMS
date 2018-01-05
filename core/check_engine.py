import datetime
from core.checker import *
from core.database_engine import *
import easysnmp


class CheckEngine:
    def run(self, host):
        if host[18] is True:
            check = Checker(host)
            host_id = host[0]
            date = datetime.datetime.now()
            ping_result = check.ping()
            if ping_result.split("|")[1] != '2':
                try:
                    self.check_snmp(host, ping_result, host_id, date)
                except easysnmp.exceptions.EasySNMPTimeoutError:
                    session = scoped_session(session_factory)
                    session = session()
                    ping = "Timed out while connecting to remote host.|1"
                    add_to_database = Check(host_id=host_id, date=date, ping=ping)
                    session.add(add_to_database)
                    session.commit()
                    session.rollback()
            else:
                session = scoped_session(session_factory)
                session = session()
                add_to_database = Check(host_id=host_id, date=date, ping=str(ping_result))
                session.add(add_to_database)
                session.commit()
                session.rollback()

    def check_snmp(self, host, ping_result, host_id, date):
        parameters_state = []
        check = Checker(host)
        parameters_state.append(ping_result)
        if host[13] is not None and host[13] != '0':
            parameters_state.append(check.interface(host[13]))
        else:
            parameters_state.append("")
        if host[14] is True or host[14] is '1':
            parameters_state.append(check.uptime())
        else:
            parameters_state.append("")
        if host[15] is True or host[15] is '1':
            parameters_state.append(check.chassis_temperature())
        else:
            parameters_state.append("")
        if host[16] is True or host[16] is '1':
            parameters_state.append(check.fan_status())
        else:
            parameters_state.append("")
        if host[17] is True or host[17] is '1':
            parameters_state.append(check.cpu_utilization())
        else:
            parameters_state.append("")
        add_to_database = Check(host_id=host_id, date=date, ping=str(parameters_state[0]),
                                interface=str(parameters_state[1]), uptime=str(parameters_state[2]),
                                chassis_temperature=str(parameters_state[3]), fan_status=str(parameters_state[4]),
                                cpu_utilization=str(parameters_state[5]))
        session = scoped_session(session_factory)
        session = session()
        session.add(add_to_database)
        session.commit()
