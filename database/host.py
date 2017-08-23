from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from core.statements import *

Base = declarative_base()


def create_base():
    Base.__tablename__ = "hosts"  # Nazwa bazy
    engine = create_engine('sqlite:///../data/hosts.db')  # Tworzmy baze ktora bedzie przechowywac dane.
    Base.metadata.create_all(engine)  # Tworzymy cala tabele. Odpowiednie do CREATE TABLE
    Base.metadata.bind = engine

    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


class Host(Base):
    create_base()
    name = Column(String(30), primary_key=True, nullable=True)  # Deklaracje pol bazy
    description = Column(String(255))
    address = Column(String(40), nullable=False, unique=True)
    snmp_version = Column(String(2), nullable=False)
    community = Column(String(30))
    security_name = Column(String(30))
    security_level = Column(String(30))
    auth_protocol = Column(String(30))
    priv_key = Column(String(30))
    priv_protocol = Column(String(30))
    auth_key = Column(String(30))

    def add(self):
        try:
            Host.session.add(self)
            Host.session.commit()
        except sqlalchemy.exc.IntegrityError as err:
            error = Statements()
            print(str(err.params[0]) + " " + error.get_statement(err))
            Host.session.rollback()
        except:
            print("Inny wyjatek")
            Host.session.rollback()


if __name__ == '__main__':
    create_base()
