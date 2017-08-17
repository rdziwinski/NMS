from core.statements import *
from multiprocessing.dummy import Pool as ThreadPool


class Multiple():
    def __init__(self, multi, func, data):
        self.multi = multi
        self.func = func
        self.data = data

    def run(self):
        try:
            pool = ThreadPool(self.multi)
            results = pool.map(self.func, self.data)
            pool.close()
            pool.join()
            return results
        except Exception as err:
            error = Statements()
            return error.get_statement(err)
