from core.host import *

poka = db.session.query(Host.description).all()
print(poka[1])


poka = db.session.query(Host).all()
print(poka[1])
