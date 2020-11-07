from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, Sequence('author_id_seq'), primary_key = True)
    firstname = Column(String)
    lastname = Column(String)

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)

Author.__table__
Base.metadata.create_all(engine)

author = Author(firstname = 'Joanne', lastname = 'Rowling')
author.firstname
author.lastname
author.id