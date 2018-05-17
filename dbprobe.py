from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fserver import User



def probe():
    engine = create_engine('sqlite:///db/database.db', echo=True)
    Session = sessionmaker(bind=engine)
    session=Session()
    for instance in session.query(User).order_by(User.id):
        print(instance.name, instance.fullname)