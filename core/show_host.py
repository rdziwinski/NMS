from core.show_status import *
from core.checker import *


class ShowHost(ShowStatus):
    def get_data(self, id):
        data = []
        data.append(self.get_name(id))
        data.append(self.get_address(id))
        data.append(self.get_description(id))
        ping = self.get_ping(id)
        data.append(self.append_parameter(ping, "list", "RTT"))
        return data

    def get_interfaces(self, id):
        data = []
        host = DatabaseEngine().get_hosts(0, id)
        check_result = Checker(host)
        interfaces = check_result.all_interfaces()
        for int, if_index in interfaces.items():
            temp = []
            temp.append(int)
            temp.append(check_result.interface_address(if_index))
            temp.append(check_result.interface_description(int))
            temp.append(check_result.interface_status(int).split("|"))
            data.append(temp)
        return data
