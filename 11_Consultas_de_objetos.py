from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, Sequence('author_id_seq'), primary_key = True)
    firstname = Column(String)
    lastname = Column(String)

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)

Base.metadata.create_all(engine)

author = Author(firstname = 'Joanne', lastname = 'Rowling')

Session = sessionmaker(bind=engine)

session = Session()

session.add(author)

session.add_all([
        Author(firstname = 'John Ronald Reuel', lastname = 'Tolkien'),
        Author(firstname = 'Jose', lastname = 'Hernandez')])

session.commit()

#Query Authors

print("Query # 1:")
for instance in session.query(Author).order_by(Author.id):
    print(instance.firstname, instance.lastname)

print("Query # 2:")
for firstname, lastname in session.query(Author.firstname, Author.lastname):
    print(firstname, lastname)

print("Query # 3:")
for row in session.query(Author, Author.firstname).all():
    print(row.Author, row.firstname)

print("Query # 4:")
for row in session.query(Author.firstname.label('firstname_label')).all():
    print(row.firstname_label)

print("Query # 5:")
author_alias = aliased(Author, name = 'author_alias')
for row in session.query(author_alias, author_alias.firstname).all():
    print(row.author_alias)

print("Query # 6:")
for an_author in session.query(Author).order_by(Author.id)[1:3]:
    print(an_author)

print("Query # 7:")
for name, in session.query(Author.firstname).filter_by(firstname = 'Joanne'):
    print(name)

print("Query # 8:")
for name, in session.query(Author.firstname).filter(Author.lastname == 'Rowling'):
    print(name)

print("Query # 9:")
for an_author in session.query(Author).\
        filter(Author.firstname == 'Joanne').\
        filter(Author.lastname == 'Rowling'):
    print(an_author)

print("Query # 10:")
print(session.query(Author).filter(Author.firstname == 'Joanne').count())