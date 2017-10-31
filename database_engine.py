from models import *
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

nowy = Host(name="aaafaa", address="192.168.1.1")
#session.add(nowy)
#session.commit()

usluga = ServicesState(date="12.12.12", uptime="45minut")

print(nowy.address)
print(usluga.uptime)
print(usluga.host_id)

#for name in session.query(Host.name):
#    print(name)
