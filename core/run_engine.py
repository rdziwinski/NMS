from multiprocessing.dummy import Pool as ThreadPool
from core.check_engine import CheckEngine
from core.show_status import *
import time
import easysnmp
import threading


class RunEngine(object):
    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            engine = CheckEngine()
            hosts = DatabaseEngine().get_hosts()
            pool = ThreadPool(128)
            try:
                pool.map(engine.run, hosts)
            except easysnmp.exceptions.EasySNMPTimeoutError:
                pool.map(engine.run, hosts)
            time.sleep(self.interval)


if __name__ == '__main__':
    engine = RunEngine(60)
    engine.run()
