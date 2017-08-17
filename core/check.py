from core.statements import *
import subprocess
import re


class Check:
    def ping(self, address):
        try:
            data = subprocess.check_output("ping " + str(address) + " -n 1")
            data = str(data)
            if "TTL" in data:
                result = re.findall('[0-9]+ms', data)
                return result[-1]
            else:
                data = re.search('from [0-9.: ]+[A-z ]+', str(data)).group().replace("from ", "")
                for_delete = re.search('[0-9.]+: ', data).group()
                result = data.replace(for_delete, "")
                return result
        except Exception as err:
            error = Statements()
            return error.get_statement(err)
