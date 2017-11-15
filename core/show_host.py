from core.show_status import *
from core.checker import *
from multiprocessing.dummy import Pool as ThreadPool


class ShowHost(ShowStatus):

    def __init__(self, id):
        self.id = id

    def get_data(self):
        data = []
        data.append(self.get_name(self.id))
        data.append(self.get_address(self.id))
        data.append(self.get_description(self.id))
        data.append(self.get_ping(self.id))
        return data

    def get_interfaces(self):
        data = []
        host = Database().get_hosts(0, self.id)
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
