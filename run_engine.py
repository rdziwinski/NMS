from multiprocessing.dummy import Pool as ThreadPool
from core.check_engine import CheckEngine
from core.show_status import *
import time
import easysnmp


class RunEngine:
    def __init__(self, interval=1, run=1):
        while run:
            engine = CheckEngine()
            hosts = Database().get_hosts()
            pool = ThreadPool(32)
            try:
                pool.map(engine.run, hosts)
            except easysnmp.exceptions.EasySNMPTimeoutError:
                pool.map(engine.run, hosts)

            time.sleep(interval)

RunEngine(1)
